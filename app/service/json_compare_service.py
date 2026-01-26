
from typing import Any, Dict, List, Optional



# Define the desired order of landmark parts
LANDMARK_PART_ORDER = ["midEyes", "leftHand", "rightHand", "lip"]
NUM_HAND_LANDMARKS = 21
NUM_LIP_LANDMARKS = 40

def _validate_landmark(landmark: Any) -> Optional[Dict[str, float]]:
    if isinstance(landmark, dict) and all(k in landmark for k in ["x", "y", "z"]):
        # Optional: Add type check for coordinates if needed
        if all(isinstance(landmark[k], (int, float)) for k in ["x", "y", "z"]):
            return landmark
    return None


def rearrange_landmark_data_concatenated_padded(
    input_data: Dict[str, Any],
) -> Dict[str, List[Dict[str, List[Optional[float]]]]]:
    # Initialize lists to hold ALL coordinate values across ALL frames
    all_x_coords: List[Optional[float]] = []
    all_y_coords: List[Optional[float]] = []
    all_z_coords: List[Optional[float]] = []

    # Calculate expected number of points per frame based on parts and padding
    points_per_frame = 0
    for part_name in LANDMARK_PART_ORDER:
        if part_name in ["leftHand", "rightHand"]:
            points_per_frame += NUM_HAND_LANDMARKS
        elif part_name == "lip":  # <--- ADD THIS ELIF
            points_per_frame += NUM_LIP_LANDMARKS
        else:
            points_per_frame += 1  # midEyes, lip

    # Safely get the list of frames
    frames: List[Dict[str, Any]] = input_data.get("frames", [])

    if not isinstance(frames, list):
        print(
            "Warning: 'frames' key does not contain a list. Returning empty data structure."
        )
        return {"data": [{"x": [], "y": [], "z": []}]}

    # Process each frame
    for frame_index, frame_data in enumerate(frames):
        # Store coordinates for the current frame before extending the main lists
        current_frame_x: List[Optional[float]] = []
        current_frame_y: List[Optional[float]] = []
        current_frame_z: List[Optional[float]] = []

        if not isinstance(frame_data, dict):
            print(
                f"Warning: Skipping invalid frame data (not a dictionary) at index {frame_index}. Padding with Nones."
            )
            # Add None placeholders for all expected points for this skipped/invalid frame
            all_x_coords.extend([None] * points_per_frame)
            all_y_coords.extend([None] * points_per_frame)
            all_z_coords.extend([None] * points_per_frame)
            continue  # Move to the next frame

        # Iterate through landmark parts in the defined order
        for part_name in LANDMARK_PART_ORDER:
            landmarks: List[Dict[str, float]] = frame_data.get(part_name, [])

            # --- Handle Hand Parts (leftHand, rightHand) ---
            if part_name in ["leftHand", "rightHand"]:
                num_landmarks_to_process = NUM_HAND_LANDMARKS
                if landmarks and isinstance(landmarks, list):
                    # Hand data exists, extract coordinates up to NUM_HAND_LANDMARKS
                    hand_x: List[Optional[float]] = []
                    hand_y: List[Optional[float]] = []
                    hand_z: List[Optional[float]] = []

                    landmarks_processed = 0
                    for i in range(num_landmarks_to_process):
                        if i < len(landmarks):
                            lm = _validate_landmark(landmarks[i])
                            if lm:
                                hand_x.append(lm.get("x"))
                                hand_y.append(lm.get("y"))
                                hand_z.append(lm.get("z"))
                                landmarks_processed += 1
                            else:
                                # Invalid landmark data within the list
                                hand_x.append(None)
                                hand_y.append(None)
                                hand_z.append(None)
                        else:
                            # Not enough landmarks provided, pad remaining
                            hand_x.append(None)
                            hand_y.append(None)
                            hand_z.append(None)

                    current_frame_x.extend(hand_x)
                    current_frame_y.extend(hand_y)
                    current_frame_z.extend(hand_z)

                else:
                    # Hand data is missing or empty, append 21 Nones
                    current_frame_x.extend([None] * num_landmarks_to_process)
                    current_frame_y.extend([None] * num_landmarks_to_process)
                    current_frame_z.extend([None] * num_landmarks_to_process)

            elif part_name == "lip":
                num_landmarks_to_process = NUM_LIP_LANDMARKS  # Use the lip constant
                if landmarks and isinstance(landmarks, list):
                    # Lip data exists, extract coordinates up to NUM_LIP_LANDMARKS
                    lip_x: List[Optional[float]] = []
                    lip_y: List[Optional[float]] = []
                    lip_z: List[Optional[float]] = []

                    for i in range(num_landmarks_to_process):
                        if i < len(landmarks):
                            lm = _validate_landmark(landmarks[i])
                            if lm:
                                lip_x.append(lm.get("x"))
                                lip_y.append(lm.get("y"))
                                lip_z.append(lm.get("z"))
                            else:
                                # Invalid landmark data within the list
                                lip_x.append(None)
                                lip_y.append(None)
                                lip_z.append(None)
                        else:
                            # Not enough landmarks provided, pad remaining
                            lip_x.append(None)
                            lip_y.append(None)
                            lip_z.append(None)

                    current_frame_x.extend(lip_x)
                    current_frame_y.extend(lip_y)
                    current_frame_z.extend(lip_z)

                else:
                    # Lip data is missing or empty, append 40 Nones
                    current_frame_x.extend([None] * num_landmarks_to_process)
                    current_frame_y.extend([None] * num_landmarks_to_process)
                    current_frame_z.extend([None] * num_landmarks_to_process)

            # --- Handle Non-Hand Parts (midEyes, lip) ---
            else:
                if landmarks and isinstance(landmarks, list) and len(landmarks) > 0:
                    # Part exists, extract coordinates of the *first* landmark
                    first_lm = _validate_landmark(landmarks[0])
                    if first_lm:
                        current_frame_x.append(first_lm.get("x"))
                        current_frame_y.append(first_lm.get("y"))
                        current_frame_z.append(first_lm.get("z"))
                    else:
                        # First landmark was invalid
                        current_frame_x.append(None)
                        current_frame_y.append(None)
                        current_frame_z.append(None)
                else:
                    # Part is missing or empty, append a single None
                    current_frame_x.append(None)
                    current_frame_y.append(None)
                    current_frame_z.append(None)

        # Extend the main coordinate lists with the data from the current frame
        NUM_DUPLICATES = 1 
        for _ in range(NUM_DUPLICATES):
            all_x_coords.extend(current_frame_x)
            all_y_coords.extend(current_frame_y)
            all_z_coords.extend(current_frame_z)


    # Construct the final output dictionary structure
    output_data = {"data": [{"x": all_x_coords, "y": all_y_coords, "z": all_z_coords}]}

    return output_data