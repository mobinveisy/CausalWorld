import argparse
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--known-meters",type=float,required=True)
    ap.add_argument("--pixel-distance",type=float,required=True); a=ap.parse_args()
    print(a.known_meters/a.pixel_distance)
if __name__=="__main__": main()
