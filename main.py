from src.feedReceiver import run_feed_recieved
from src.feedCombiner import run_feed_combiner

if __name__ == "__main__":
    camera0_proc, camera1_proc = run_feed_recieved(return_processes=True)
    for combined_frame in run_feed_combiner(camera0_proc, camera1_proc):
        print("✅ Combined frame received with shape:", combined_frame.shape)

