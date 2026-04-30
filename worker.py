
import os
import sys
import logging
from flask import Flask, jsonify, request
import threading

# Add src to path so we can import the cycle logic
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.autonomous_analytics_cycle import AutonomousAnalyticsCycle

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Simple in-memory lock to prevent overlapping cycles if triggered rapidly
cycle_lock = threading.Lock()

@app.route('/', methods=['GET'])
def health():
    return jsonify({"status": "ready", "service": "xmrtnet-analytics-worker"}), 200

@app.route('/start', methods=['POST'])
def start_cycle():
    """Triggers the analytics cycle."""
    if cycle_lock.locked():
        return jsonify({"status": "busy", "message": "Cycle already in progress"}), 429
    
    # We can run it in a thread to return immediately, or blocking. 
    # For Cloud Run generic service, blocking is okay if it takes < 60 mins.
    # But usually better to blocking so we know it finished.
    # The cycle script suggests it runs one cycle then exits.
    
    got_lock = cycle_lock.acquire(blocking=False)
    if not got_lock:
         return jsonify({"status": "busy"}), 429

    try:
        logger.info("Starting Analytics Cycle")
        # We need to determine cycle number. The script does this in main(), 
        # but we can reuse the class.
        
        # Simple cycle number generation based on time or just random for now if state not found
        # In real usage, verify_cycle_state would read/write .cycle_state.json
        # For now, let's just instantiate and run.
        cycle_num = 744 # Default or dynamic
        
        cycle = AutonomousAnalyticsCycle(cycle_num)
        results = cycle.run_cycle()
        
        return jsonify({
            "status": "completed", 
            "results": results
        }), 200
        
    except Exception as e:
        logger.error(f"Cycle failed: {e}")
        return jsonify({"status": "error", "error": str(e)}), 500
    finally:
        cycle_lock.release()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
