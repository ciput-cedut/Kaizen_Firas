"""
Test script to verify USB-C display detection
Run this to see what input codes your monitors report
"""
from monitorcontrol import get_monitors

print("=" * 60)
print("USB-C Display Port Detection Test")
print("=" * 60)

for i, monitor in enumerate(get_monitors()):
    print(f"\n📺 Monitor {i + 1}:")
    try:
        with monitor:
            caps = monitor.get_vcp_capabilities()
            inputs = caps.get('inputs', [])
            
            if not inputs:
                print("  ⚠ No inputs detected")
                continue
                
            print(f"  Found {len(inputs)} input(s):")
            for inp in inputs:
                if hasattr(inp, 'name'):
                    # Standard InputSource enum value
                    print(f"    ✓ {inp.name} (Code: {inp.value})")
                elif isinstance(inp, int):
                    # Raw integer code - check for USB-C
                    if inp == 27:
                        print(f"    🔌 USB-C with DisplayPort Alt Mode (Code: {inp})")
                    elif inp == 26:
                        print(f"    ⚡ Thunderbolt (Code: {inp})")
                    else:
                        print(f"    ? Unknown Input Type (Code: {inp})")
                        
    except Exception as e:
        print(f"  ❌ Error: {e}")

print("\n" + "=" * 60)
print("Input Code Reference:")
print("  Code 15, 16 = DisplayPort (DP1, DP2)")
print("  Code 17, 18 = HDMI (HDMI1, HDMI2)")
print("  Code 26 = Thunderbolt")
print("  Code 27 = USB-C with DP Alt Mode")
print("=" * 60)
