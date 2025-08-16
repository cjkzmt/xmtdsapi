
import cv2
def 单视频裁剪(video_path, 视频宽, 视频高, output_path, f):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error opening video {video_path}")
        return
    fps = cap.get(cv2.CAP_PROP_FPS)
    frames = []
    while True:
        ret, frame = cap.read()
        if not ret: break
        if f == 'left': cropped_frame = frame[:, :视频宽]
        elif f == 'right': cropped_frame = frame[:, -视频宽:]
        elif f == 'center':
            x = frame.shape[1] // 2 - 视频宽 // 2
            cropped_frame = frame[:, x:x + 视频宽]
        cropped_frame = cv2.resize(cropped_frame, (视频宽, 视频高))
        frames.append(cropped_frame)
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (视频宽, 视频高))
    for frame in frames:
        out.write(frame)
    out.release()

def 视频水平镜像(input_path, output_path):
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))
    while True:
        ret, frame = cap.read()
        if not ret:break
        mirrored_frame = cv2.flip(frame, 1)
        out.write(mirrored_frame)
    cap.release()
    out.release()