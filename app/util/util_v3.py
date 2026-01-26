from copy import copy
import torch
import numpy as np

def convert_to_row_dict(left_hand, right_hand):
        """
        Chuyển đổi từ ndarray [T, 21, 3] sang dict dạng {"wrist_0": [[x, y, z], ...], ...}
        """
        identifiers = [
            "wrist", "thumbCMC", "thumbMP", "thumbIP", "thumbTip",
            "indexMCP", "indexPIP", "indexDIP", "indexTip",
            "middleMCP", "middlePIP", "middleDIP", "middleTip",
            "ringMCP", "ringPIP", "ringDIP", "ringTip",
            "littleMCP", "littlePIP", "littleDIP", "littleTip"
        ]
        T = left_hand.shape[0]
        row = {}
        for i in range(21):
            row[f"{identifiers[i]}_0"] = left_hand[:, i, :].tolist()
            row[f"{identifiers[i]}_1"] = right_hand[:, i, :].tolist()
        return row


def normalize_hand(row: dict):
        HAND_IDENTIFIERS = [
            "wrist", "indexTip", "indexDIP", "indexPIP", "indexMCP",
            "middleTip", "middleDIP", "middlePIP", "middleMCP",
            "ringTip", "ringDIP", "ringPIP", "ringMCP",
            "littleTip", "littleDIP", "littlePIP", "littleMCP",
            "thumbTip", "thumbIP", "thumbMP", "thumbCMC"
        ]

        row = copy.deepcopy(row)
        hand_landmarks = {0: [], 1: []}
        num_hands = 2 if "wrist_1" in row else 1

        for identifier in HAND_IDENTIFIERS:
            for hand_index in range(num_hands):
                hand_landmarks[hand_index].append(f"{identifier}_{hand_index}")

        for hand_index in range(num_hands):
            sequence_size = len(row[f"wrist_{hand_index}"])
            for seq_idx in range(sequence_size):
                x_vals = [row[k][seq_idx][0] for k in hand_landmarks[hand_index] if row[k][seq_idx][0] != 0]
                y_vals = [row[k][seq_idx][1] for k in hand_landmarks[hand_index] if row[k][seq_idx][1] != 0]
                z_vals = [row[k][seq_idx][2] for k in hand_landmarks[hand_index] if row[k][seq_idx][2] != 0]

                if not x_vals or not y_vals or not z_vals:
                    continue

                width = max(x_vals) - min(x_vals)
                height = max(y_vals) - min(y_vals)
                depth = max(z_vals) - min(z_vals)

                if width == 0 or height == 0 or depth == 0:
                    continue

                if width > height:
                    delta_x = 0.1 * width
                    delta_y = delta_x + (width - height) / 2
                else:
                    delta_y = 0.1 * height
                    delta_x = delta_y + (height - width) / 2

                delta_z = 0.1 * depth

                start_x, end_x = min(x_vals) - delta_x, max(x_vals) + delta_x
                start_y, end_y = min(y_vals) - delta_y, max(y_vals) + delta_y
                start_z, end_z = min(z_vals) - delta_z, max(z_vals) + delta_z

                for identifier in HAND_IDENTIFIERS:
                    key = f"{identifier}_{hand_index}"
                    x, y, z = row[key][seq_idx]
                    if x == 0 or y == 0 or z == 0:
                        continue
                    norm_x = (x - start_x) / (end_x - start_x) if (end_x - start_x) != 0 else 0
                    norm_y = (y - start_y) / (end_y - start_y) if (end_y - start_y) != 0 else 0
                    norm_z = (z - start_z) / (end_z - start_z) if (end_z - start_z) != 0 else 0
                    row[key][seq_idx] = [norm_x, norm_y, norm_z]

        return row

def normalize_hand_v2(row: dict):
        import copy
        HAND_IDENTIFIERS = [
            "wrist", "indexTip", "indexDIP", "indexPIP", "indexMCP",
            "middleTip", "middleDIP", "middlePIP", "middleMCP",
            "ringTip", "ringDIP", "ringPIP", "ringMCP",
            "littleTip", "littleDIP", "littlePIP", "littleMCP",
            "thumbTip", "thumbIP", "thumbMP", "thumbCMC"
        ]

        body_ref_key = "body_ref_point"  # điểm cơ thể làm gốc tham chiếu

        row = copy.deepcopy(row)
        hand_landmarks = {0: [], 1: []}
        num_hands = 2 if "wrist_1" in row else 1

        for identifier in HAND_IDENTIFIERS:
            for hand_index in range(num_hands):
                hand_landmarks[hand_index].append(f"{identifier}_{hand_index}")

        # Tính tọa độ tương đối so với body_ref_key
        if body_ref_key in row:
            sequence_size = len(row[body_ref_key])
            for hand_index in range(num_hands):
                for seq_idx in range(sequence_size):
                    x0, y0, z0 = row[body_ref_key][seq_idx]
                    if x0 == 0 and y0 == 0 and z0 == 0:
                        continue  # bỏ qua nếu điểm cơ thể không phát hiện được

                    for identifier in HAND_IDENTIFIERS:
                        key = f"{identifier}_{hand_index}"
                        if key not in row or seq_idx >= len(row[key]):
                            continue

                        x, y, z = row[key][seq_idx]
                        if x == 0 or y == 0 or z == 0:
                            continue

                        # cập nhật giá trị thành tương đối so với cơ thể
                        row[key][seq_idx] = [x - x0, y - y0, z - z0]

        # Chuẩn hóa relative position
        for hand_index in range(num_hands):
            sequence_size = len(row[f"wrist_{hand_index}"])
            for seq_idx in range(sequence_size):
                x_vals = [row[k][seq_idx][0] for k in hand_landmarks[hand_index] if row[k][seq_idx][0] != 0]
                y_vals = [row[k][seq_idx][1] for k in hand_landmarks[hand_index] if row[k][seq_idx][1] != 0]
                z_vals = [row[k][seq_idx][2] for k in hand_landmarks[hand_index] if row[k][seq_idx][2] != 0]

                if not x_vals or not y_vals or not z_vals:
                    continue

                width = max(x_vals) - min(x_vals)
                height = max(y_vals) - min(y_vals)
                depth = max(z_vals) - min(z_vals)

                if width == 0 or height == 0 or depth == 0:
                    continue

                if width > height:
                    delta_x = 0.1 * width
                    delta_y = delta_x + (width - height) / 2
                else:
                    delta_y = 0.1 * height
                    delta_x = delta_y + (height - width) / 2

                delta_z = 0.1 * depth

                start_x, end_x = min(x_vals) - delta_x, max(x_vals) + delta_x
                start_y, end_y = min(y_vals) - delta_y, max(y_vals) + delta_y
                start_z, end_z = min(z_vals) - delta_z, max(z_vals) + delta_z

                for identifier in HAND_IDENTIFIERS:
                    key = f"{identifier}_{hand_index}"
                    x, y, z = row[key][seq_idx]
                    if x == 0 or y == 0 or z == 0:
                        continue
                    norm_x = (x - start_x) / (end_x - start_x) if (end_x - start_x) != 0 else 0
                    norm_y = (y - start_y) / (end_y - start_y) if (end_y - start_y) != 0 else 0
                    norm_z = (z - start_z) / (end_z - start_z) if (end_z - start_z) != 0 else 0
                    row[key][seq_idx] = [norm_x, norm_y, norm_z]

        return row


def process_data(X, version):
    """
    Xử lý dữ liệu landmark bằng cách áp dụng frame drop và chuẩn hóa.

    Input:
    - X: Tensor chứa dữ liệu landmark (left hand, right hand, Lips) (B, 3xP, T).

    Output:
    - landmark: tensor đã được xử lý (B, 3XP, T).
    """
    dict = ["left_hand", "right_hand", "lips"]
    X = X.permute(1, 0, 2)  #(246, 16, 30) 
    T = X.size(-1)
    X = X.view(82, 3, X.shape[1], X.shape[2])
    X = X.permute(2, 3, 0, 1)

    l_hand = X[:, :, :21, :] 
    r_hand = X[:, :, 21:42, :]
    body = X[:, :, 42:, :] 
    
    landmark_dict = {
    "left_hand": np.zeros((T, 21, 3)),
    "right_hand": np.zeros((T, 21, 3)),
    "lips": np.zeros((T, 40, 3))
    }

    row = convert_to_row_dict(torch.squeeze(l_hand, dim=0), torch.squeeze(r_hand, dim=0))
    if version == 1:
        row = normalize_hand(row)
    else:
        row = normalize_hand_v2(row)
    identifiers = [
    "wrist", "thumbCMC", "thumbMP", "thumbIP", "thumbTip",
    "indexMCP", "indexPIP", "indexDIP", "indexTip",
    "middleMCP", "middlePIP", "middleDIP", "middleTip",
    "ringMCP", "ringPIP", "ringDIP", "ringTip",
    "littleMCP", "littlePIP", "littleDIP", "littleTip"
    ]
    for i in range(21):
        landmark_dict["left_hand"][:, i, :] = np.array(row[f"{identifiers[i]}_0"])
        landmark_dict["right_hand"][:, i, :] = np.array(row[f"{identifiers[i]}_1"])

    landmark = np.concatenate([landmark_dict[key] for key in dict], axis=1)
    landmark = torch.tensor(landmark, dtype=torch.float32)
    
    landmark[torch.isnan(landmark)] = 0.0
    landmark = landmark.reshape(landmark.shape[0], -1)
    landmark = torch.permute(landmark, (1, 0))  # (3P, T)
    return landmark