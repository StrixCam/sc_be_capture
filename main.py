from src.feedReceiver import run_feed_recieved
from src.feedCombiner import run_feed_combiner
from src.feedSender import run_feed_sender

if __name__ == "__main__":
    result = run_feed_recieved(return_processes=True)
    if result is None:
        raise RuntimeError("run_feed_recieved did not return camera processes")

    camera0_proc, camera1_proc = result

    combined_frames = run_feed_combiner(camera0_proc, camera1_proc)
    run_feed_sender(combined_frames)
