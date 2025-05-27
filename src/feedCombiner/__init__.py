from .feedCombiner import combine_camera_feeds

def run_feed_combiner(process_0, process_1):
    """
    Runs the feed combiner with the provided camera processes.
    
    Args:
        process_0 (subprocess.Popen): The first camera process.
        process_1 (subprocess.Popen): The second camera process.
    
    Yields:
        np.ndarray: Combined frames from both camera feeds.
    """
    try:
        for combined_frame in combine_camera_feeds(process_0, process_1):
            yield combined_frame
    except Exception as e:
        print(f"⚠️ Error in feed combiner: {e}")
    finally:
        process_0.terminate()
        process_1.terminate()