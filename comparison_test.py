"""
Comprehensive Performance Comparison: gRPC vs FastAPI
Supports multiple words/test cases and generates per-word comparison sections.
"""

import requests
import time
import json
import sys
import argparse
from pathlib import Path
import random

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import grpc
from grpc_service import sign_recognition_pb2 as pb2
from grpc_service import sign_recognition_pb2_grpc as pb2_grpc

# Random frame data generator for test cases
def generate_random_frame_data(
    seed=None,
    left_center=(0.25, 0.55),
    right_center=(0.85, 0.55),
    jitter=0.12,
    depth_range=(-0.05, 0.20),
    include_lip=False,
):
    """Generate a randomized frame data structure with 21 landmarks per hand.

    - seed: optional seed for reproducibility
    - left_center/right_center: nominal centers for each hand (x, y)
    - jitter: max uniform offset around centers
    - depth_range: min/max z values
    - include_lip: if True, add simple randomized lip landmarks
    """
    rng = random.Random(seed)

    midEyes = {"x": 0.5, "y": 0.5, "z": 0.1}

    def sample_point(cx, cy):
        x = max(0.0, min(1.2, cx + rng.uniform(-jitter, jitter)))
        y = max(0.0, min(1.0, cy + rng.uniform(-jitter, jitter)))
        z = rng.uniform(depth_range[0], depth_range[1])
        return {"x": x, "y": y, "z": z}

    leftHand = [sample_point(left_center[0], left_center[1]) for _ in range(21)]
    rightHand = [sample_point(right_center[0], right_center[1]) for _ in range(21)]

    lip = []
    if include_lip:
        lip = [sample_point(0.5, 0.65) for _ in range(10)]

    return {"midEyes": midEyes, "leftHand": leftHand, "rightHand": rightHand, "lip": lip}

# Define the words/test cases you want to exercise. Duplicate entries with new frame_data to test other signs.
TEST_CASES = [
    {
        "name": "random_frame_1",
        "frame_data": generate_random_frame_data(seed=None),  # Truly random
        "previous_word": "",
        "platform": "web",
        "language_code": "vn",
        "num_requests": 10,
    },
]

# Convert structured data to flat array for FastAPI
def convert_to_flat_array(frame_data):
    """Convert structured frame data to flat coordinate array"""
    flat = [[frame_data["midEyes"]["x"], frame_data["midEyes"]["y"], frame_data["midEyes"]["z"]]]
    for point in frame_data["leftHand"]:
        flat.append([point["x"], point["y"], point["z"]])
    for point in frame_data["rightHand"]:
        flat.append([point["x"], point["y"], point["z"]])
    for point in frame_data["lip"]:
        flat.append([point["x"], point["y"], point["z"]])
    return flat

def build_grpc_request(frame_data, previous_word, platform, language_code):
    mid = pb2.Landmark(
        x=frame_data["midEyes"]["x"],
        y=frame_data["midEyes"]["y"],
        z=frame_data["midEyes"]["z"],
    )
    left_hand = [pb2.Landmark(x=p["x"], y=p["y"], z=p["z"]) for p in frame_data["leftHand"]]
    right_hand = [pb2.Landmark(x=p["x"], y=p["y"], z=p["z"]) for p in frame_data["rightHand"]]
    lip = [pb2.Landmark(x=p["x"], y=p["y"], z=p["z"]) for p in frame_data["lip"]]
    frame = pb2.Frame(midEyes=mid, leftHand=left_hand, rightHand=right_hand, lip=lip)
    return pb2.RecognizeRequest(frames=[frame], previous_word=previous_word, platform=platform, language_code=language_code)


def test_grpc(case, host="localhost", port=50051, num_requests=None):
    """Test gRPC performance for a single case"""
    results = {
        "framework": "gRPC",
        "times": [],
        "signs": [],
        "confidences": [],
        "errors": 0,
        "total_sizes": 0,
    }
    requested = num_requests if num_requests is not None else case.get("num_requests", 10)
    results["requested_requests"] = requested
    # Use the exact same frame data for every gRPC request so it's identical to the FastAPI run
    shared_frame_data = case["frame_data"]
    try:
        with grpc.insecure_channel(f"{host}:{port}") as channel:
            stub = pb2_grpc.SignRecognitionServiceStub(channel)

            for req_num in range(1, requested + 1):
                req = build_grpc_request(
                    frame_data=shared_frame_data,
                    previous_word=case["previous_word"],
                    platform=case["platform"],
                    language_code=case["language_code"],
            )

                start = time.time()
                resp = stub.Recognize(req)
                elapsed = (time.time() - start) * 1000
                results["times"].append(elapsed)

                if resp.error:
                    results["errors"] += 1
                    print(f"  [gRPC Req #{req_num}] ❌ Error - {elapsed:.2f}ms")
                else:
                    sign = "unknown"
                    for r in resp.results:
                        results["signs"].append(r.class_name)
                        results["confidences"].append(float(r.confidence))
                        sign = r.class_name
                        break
                    print(f"  [gRPC Req #{req_num}] ✓ {elapsed:.2f}ms - Sign: {sign}")

        req_pb = req.SerializeToString()
        results["request_size"] = len(req_pb)
        results["executed_requests"] = len(results["times"])
        results["avg_confidence"] = (
            sum(results["confidences"]) / len(results["confidences"])
            if results["confidences"]
            else 0
        )
        return results

    except Exception as e:
        print(f"gRPC Error ({case['name']}): {e}")
        return None


def test_fastapi(case, host="localhost", port=8000, num_requests=None):
    """Test FastAPI performance for a single case"""
    results = {
        "framework": "FastAPI",
        "times": [],
        "signs": [],
        "confidences": [],
        "errors": 0,
    }

    url = f"http://{host}:{port}/v3/api/sign-language/recognize?platform={case['platform']}&language_code={case['language_code']}"
    request_payload = {
        "frames": [convert_to_flat_array(case["frame_data"])],
        "platform": case["platform"],
        "language_code": case["language_code"],
        "previous_word": case["previous_word"],
    }

    requested = num_requests if num_requests is not None else case.get("num_requests", 10)
    results["requested_requests"] = requested
    try:
        for i in range(requested):
            start = time.time()
            response = requests.post(url, json=request_payload, timeout=10)
            elapsed = (time.time() - start) * 1000
            results["times"].append(elapsed)

            if response.status_code != 200:
                results["errors"] += 1
                if i == 0:
                    print(f"FastAPI Error ({case['name']}): Status {response.status_code}, Response: {response.text}")
            else:
                data = response.json()
                if "data" in data:
                    for r in data["data"]:
                        sign_val = r.get("class") or r.get("Class") or "unknown"
                        conf_val = r.get("confidence") or r.get("Confidence") or 0
                        results["signs"].append(sign_val)
                        results["confidences"].append(float(conf_val))
                        break

        req_json = json.dumps(request_payload).encode()
        results["request_size"] = len(req_json)
        results["executed_requests"] = len(results["times"])
        results["avg_confidence"] = (
            sum(results["confidences"]) / len(results["confidences"])
            if results["confidences"]
            else 0
        )
        return results

    except Exception as e:
        print(f"FastAPI Error ({case['name']}): {e}")
        return None


def safe_stats(times):
    if not times:
        return {"avg": 0, "min": 0, "max": 0, "std": 0, "throughput": 0}
    avg = sum(times) / len(times)
    variance = sum((x - avg) ** 2 for x in times) / len(times)
    std = variance ** 0.5
    throughput = len(times) * 1000 / sum(times) if sum(times) else 0
    return {"avg": avg, "min": min(times), "max": max(times), "std": std, "throughput": throughput}


def generate_report(case_results):
    """Generate comparison report for all cases"""
    now = time.strftime('%Y-%m-%d %H:%M:%S')
    report_lines = [
        "# Performance Comparison: gRPC vs FastAPI",
        "## Sign Language Recognition Service",
        f"**Test Date:** {now}",
        "**Test Data:** Vietnamese Sign Language (Teledeaf)",
        "",
        "---",
    ]

    for idx, entry in enumerate(case_results, start=1):
        case = entry["case"]
        grpc_results = entry["grpc"]
        fastapi_results = entry["fastapi"]
        grpc_stats = safe_stats(grpc_results["times"])
        fastapi_stats = safe_stats(fastapi_results["times"])

        report_lines.extend(
            [
                f"\n## Case {idx}: {case['name']}",
                f"**Requests Executed:** gRPC {grpc_results.get('executed_requests', len(grpc_results['times']))}/{grpc_results.get('requested_requests', 'n/a')} | FastAPI {fastapi_results.get('executed_requests', len(fastapi_results['times']))}/{fastapi_results.get('requested_requests', 'n/a')}",
                f"**Previous Word:** {case['previous_word']}",
                f"**Language:** {case['language_code']}",
                "",
                "### 1. Response Time Comparison",
                "#### gRPC Results:",
                f"- Average Response Time: **{grpc_stats['avg']:.2f} ms**",
                f"- Min Response Time: {grpc_stats['min']:.2f} ms",
                f"- Max Response Time: {grpc_stats['max']:.2f} ms",
                f"- Std Deviation: {grpc_stats['std']:.2f} ms",
                "",
                "#### FastAPI Results:",
                f"- Average Response Time: **{fastapi_stats['avg']:.2f} ms**",
                f"- Min Response Time: {fastapi_stats['min']:.2f} ms",
                f"- Max Response Time: {fastapi_stats['max']:.2f} ms",
                f"- Std Deviation: {fastapi_stats['std']:.2f} ms",
                "",
            ]
        )

        if grpc_stats["avg"] and fastapi_stats["avg"]:
            if grpc_stats["avg"] < fastapi_stats["avg"]:
                improvement = ((fastapi_stats["avg"] - grpc_stats["avg"]) / fastapi_stats["avg"]) * 100
                report_lines.append(f"**Performance Winner:** ✅ gRPC is {improvement:.1f}% faster than FastAPI")
            else:
                improvement = ((grpc_stats["avg"] - fastapi_stats["avg"]) / grpc_stats["avg"]) * 100
                report_lines.append(f"**Performance Winner:** ✅ FastAPI is {improvement:.1f}% faster than gRPC")
        else:
            report_lines.append("**Performance Winner:** N/A (no timing data)")

        report_lines.extend(
            [
                "",
                "### 2. Throughput Comparison",
                f"- gRPC Throughput: **{grpc_stats['throughput']:.2f} requests/second**",
                f"- FastAPI Throughput: **{fastapi_stats['throughput']:.2f} requests/second**",
                "",
                "### 3. Message Size Comparison",
                f"- gRPC Request Size (Binary): **{grpc_results.get('request_size', 0)} bytes**",
                "- Serialization: Protocol Buffers (Binary)",
                f"- FastAPI Request Size (JSON): **{fastapi_results.get('request_size', 0)} bytes**",
                "- Serialization: JSON (Text)",
            ]
        )

        if grpc_results.get("request_size") and fastapi_results.get("request_size") and grpc_results["request_size"] < fastapi_results["request_size"]:
            reduction = ((fastapi_results["request_size"] - grpc_results["request_size"]) / fastapi_results["request_size"]) * 100
            report_lines.append(f"- Size Winner: ✅ gRPC sends {reduction:.1f}% smaller messages")

        # Add per-request time comparison table
        report_lines.extend([
            "",
            "### 3.5. Per-Request Time Comparison",
            "",
            "| Request # | gRPC (ms) | FastAPI (ms) | Difference (ms) | FastAPI % Slower |",
            "|-----------|-----------|--------------|-----------------|------------------|",
        ])
        
        min_requests = min(len(grpc_results["times"]), len(fastapi_results["times"]))
        for i in range(min_requests):
            grpc_time = grpc_results["times"][i]
            fastapi_time = fastapi_results["times"][i]
            diff = fastapi_time - grpc_time
            percent_slower = ((fastapi_time - grpc_time) / grpc_time * 100) if grpc_time > 0 else 0
            report_lines.append(f"| {i+1} | {grpc_time:.2f} | {fastapi_time:.2f} | {diff:.2f} | {percent_slower:.1f}% |")

        report_lines.extend(
            [
                "",
                "### 4. Accuracy/Recognition Consistency",
                f"- gRPC Recognized Sign: **{grpc_results['signs'][0] if grpc_results['signs'] else 'N/A'}**",
                f"- gRPC Average Confidence: {grpc_results.get('avg_confidence', 0):.4f}",
                f"- gRPC Unique Signs: {len(set(grpc_results['signs']))}",
                f"- gRPC Error Rate: {(grpc_results['errors'] / len(grpc_results['times']) * 100) if grpc_results['times'] else 0:.1f}%",
                f"- FastAPI Recognized Sign: **{fastapi_results['signs'][0] if fastapi_results['signs'] else 'N/A'}**",
                f"- FastAPI Average Confidence: {fastapi_results.get('avg_confidence', 0):.4f}",
                f"- FastAPI Unique Signs: {len(set(fastapi_results['signs']))}",
                f"- FastAPI Error Rate: {(fastapi_results['errors'] / len(fastapi_results['times']) * 100) if fastapi_results['times'] else 0:.1f}%",
                "",
                "---",
            ]
        )

    return "\n".join(report_lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test gRPC and/or FastAPI performance")
    parser.add_argument(
        "--mode",
        choices=["grpc", "fastapi", "both"],
        default="both",
        help="Test mode: grpc only, fastapi only, or both (default: both)"
    )
    parser.add_argument(
        "--host",
        default="localhost",
        help="Server host (default: localhost)"
    )
    parser.add_argument(
        "--grpc-port",
        type=int,
        default=50051,
        help="gRPC server port (default: 50051)"
    )
    parser.add_argument(
        "--fastapi-port",
        type=int,
        default=8000,
        help="FastAPI server port (default: 8000)"
    )
    parser.add_argument(
        "--requests",
        type=int,
        help="Override number of requests per test case (default: use case num_requests)"
    )
    
    args = parser.parse_args()

    print("\n" + "="*60)
    if args.mode == "both":
        print("PERFORMANCE COMPARISON: gRPC vs FastAPI")
    elif args.mode == "grpc":
        print("gRPC PERFORMANCE TEST")
    else:
        print("FastAPI PERFORMANCE TEST")
    print("="*60 + "\n")

    case_results = []
    for case in TEST_CASES:
        grpc_results = None
        fastapi_results = None
        
        if args.mode in ["grpc", "both"]:
            print(f"⏳ Testing gRPC for case: {case['name']}...")
            grpc_results = test_grpc(case, host=args.host, port=args.grpc_port, num_requests=args.requests)
            if grpc_results:
                print(f"✅ gRPC test completed for {case['name']}")
                if args.mode == "grpc":
                    stats = safe_stats(grpc_results["times"])
                    print(f"   - Requests executed: {grpc_results.get('executed_requests', 0)}/{grpc_results.get('requested_requests', 'n/a')}")
                    print(f"   - Average Response Time: {stats['avg']:.2f} ms")
                    print(f"   - Throughput: {stats['throughput']:.2f} req/s")
                    print(f"   - Recognized Sign: {grpc_results['signs'][0] if grpc_results['signs'] else 'N/A'}")
                    print(f"   - Confidence: {grpc_results.get('avg_confidence', 0):.4f}")

        if args.mode in ["fastapi", "both"]:
            print(f"⏳ Testing FastAPI for case: {case['name']}...")
            fastapi_results = test_fastapi(case, host=args.host, port=args.fastapi_port, num_requests=args.requests)
            if fastapi_results:
                print(f"✅ FastAPI test completed for {case['name']}")
                if args.mode == "fastapi":
                    stats = safe_stats(fastapi_results["times"])
                    print(f"   - Requests executed: {fastapi_results.get('executed_requests', 0)}/{fastapi_results.get('requested_requests', 'n/a')}")
                    print(f"   - Average Response Time: {stats['avg']:.2f} ms")
                    print(f"   - Throughput: {stats['throughput']:.2f} req/s")
                    print(f"   - Recognized Sign: {fastapi_results['signs'][0] if fastapi_results['signs'] else 'N/A'}")
                    print(f"   - Confidence: {fastapi_results.get('avg_confidence', 0):.4f}")

        if args.mode == "both" and grpc_results and fastapi_results:
            case_results.append({"case": case, "grpc": grpc_results, "fastapi": fastapi_results})
        elif args.mode != "both" and (grpc_results or fastapi_results):
            # For single mode tests, we still collect results but won't generate comparison report
            pass
        else:
            print(f"❌ Test failed for case {case['name']}")

    if args.mode == "both" and case_results:
        report = generate_report(case_results)

        report_path = Path(__file__).parent / "comparison_report.md"
        report_path.write_text(report, encoding="utf-8")

        print("\n" + report)
        print(f"\n✅ Report saved to: {report_path}")
    elif args.mode == "both" and not case_results:
        print("\n❌ All tests failed. Make sure both servers are running!")
        print("Terminal 1: python -m grpc_service.server.main")
        print("Terminal 2: python -m app.api.api_main")
    elif args.mode == "grpc":
        print("\n✅ gRPC testing completed!")
        print("To start gRPC server: python -m grpc_service.server.main")
    elif args.mode == "fastapi":
        print("\n✅ FastAPI testing completed!")
        print("To start FastAPI server: python -m app.api.api_main")
