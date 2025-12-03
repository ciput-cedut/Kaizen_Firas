"""
Direct Monitor Input Code Detection Tool

This script queries all connected monitors via DDC/CI protocol
and displays the raw input codes they support.

Usage: python detect_monitor_inputs.py
"""

from monitorcontrol import get_monitors, InputSource
import sys

def get_input_name(code):
    """Convert input code to readable name"""
    # Standard InputSource enum mapping
    standard_inputs = {
        0: "OFF",
        1: "ANALOG1/VGA",
        2: "ANALOG2",
        3: "DVI1",
        4: "DVI2",
        5: "COMPOSITE1",
        6: "COMPOSITE2",
        7: "SVIDEO1",
        8: "SVIDEO2",
        9: "TUNER1",
        10: "TUNER2",
        11: "TUNER3",
        12: "COMPONENT1",
        13: "COMPONENT2",
        14: "COMPONENT3",
        15: "DP1 (DisplayPort 1)",
        16: "DP2 (DisplayPort 2)",
        17: "HDMI1",
        18: "HDMI2",
        26: "THUNDERBOLT",
        27: "USB-C (DisplayPort Alt Mode)"
    }
    
    return standard_inputs.get(code, f"UNKNOWN CODE {code}")

def detect_monitors():
    """Detect all monitors and their input codes"""
    print("=" * 70)
    print("MONITOR INPUT CODE DETECTOR")
    print("=" * 70)
    print()
    
    monitors = list(get_monitors())
    
    if not monitors:
        print("❌ No monitors detected!")
        print("   Make sure your monitors support DDC/CI")
        return
    
    print(f"Found {len(monitors)} monitor(s)\n")
    
    for i, monitor in enumerate(monitors):
        print(f"{'='*70}")
        print(f"📺 MONITOR #{i + 1}")
        print(f"{'='*70}")
        
        try:
            with monitor:
                # Get VCP capabilities
                caps = monitor.get_vcp_capabilities()
                
                # Get current input
                try:
                    current_input = monitor.get_input_source()
                    if hasattr(current_input, 'value'):
                        current_code = current_input.value
                        current_name = current_input.name if hasattr(current_input, 'name') else str(current_input)
                    else:
                        current_code = int(current_input)
                        current_name = get_input_name(current_code)
                    print(f"🟢 Current Input: {current_name} (Code: {current_code})")
                except Exception as e:
                    print(f"⚠️  Could not read current input: {e}")
                    current_code = None
                
                print()
                
                # Get available inputs
                inputs = caps.get('inputs', [])
                
                if not inputs:
                    print("⚠️  No input list found in capabilities")
                else:
                    print(f"Available Inputs ({len(inputs)}):")
                    print("-" * 70)
                    
                    for inp in inputs:
                        # Check if it's an InputSource enum or raw integer
                        if hasattr(inp, 'name') and hasattr(inp, 'value'):
                            # Standard InputSource enum
                            code = inp.value
                            name = inp.name
                            source = "Standard"
                        elif isinstance(inp, int):
                            # Raw integer code (custom/non-standard)
                            code = inp
                            name = get_input_name(code)
                            source = "Custom"
                        else:
                            # Unknown format
                            code = "Unknown"
                            name = str(inp)
                            source = "Unknown"
                        
                        # Mark current input
                        marker = " ◄── ACTIVE" if (current_code is not None and code == current_code) else ""
                        
                        print(f"  [{source:8}] Code {code:3} → {name}{marker}")
                
                # Display other capabilities
                print()
                print("Other Capabilities:")
                print("-" * 70)
                for key, value in caps.items():
                    if key != 'inputs':
                        print(f"  {key}: {value}")
                        
        except Exception as e:
            print(f"❌ ERROR: {e}")
            print(f"   This monitor may not support DDC/CI communication")
        
        print()
    
    print("=" * 70)
    print("DETECTION COMPLETE")
    print("=" * 70)
    print()
    print("Input Code Reference:")
    print("  • Codes 15-18: DisplayPort and HDMI (standard)")
    print("  • Code 26: Thunderbolt")
    print("  • Code 27: USB-C with DisplayPort Alt Mode")
    print("  • Code 1-2: Analog/VGA")
    print("  • Code 3-4: DVI")
    print()

if __name__ == "__main__":
    try:
        detect_monitors()
    except KeyboardInterrupt:
        print("\n\n⚠️  Detection cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        sys.exit(1)
