import argparse,csv
from pathlib import Path
import cv2,numpy as np
def center(c): return np.asarray(c,np.float32).reshape(-1,2).mean(0)
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--video",required=True); ap.add_argument("--output",required=True)
    ap.add_argument("--marker-a",type=int,required=True); ap.add_argument("--marker-b",type=int,required=True)
    a=ap.parse_args(); dic=cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
    det=cv2.aruco.ArucoDetector(dic,cv2.aruco.DetectorParameters()); cap=cv2.VideoCapture(a.video); fps=cap.get(cv2.CAP_PROP_FPS)
    last={a.marker_a:(np.nan,np.nan),a.marker_b:(np.nan,np.nan)}; rows=[]; i=0
    while True:
        ok,fr=cap.read()
        if not ok: break
        corners,ids,_=det.detectMarkers(fr)
        if ids is not None:
            for c,mid in zip(corners,ids.flatten()):
                if int(mid) in last: last[int(mid)]=tuple(map(float,center(c)))
        ax,ay=last[a.marker_a]; bx,by=last[a.marker_b]
        rows.append(dict(frame=i,time_s=i/fps,a_x_px=ax,a_y_px=ay,b_x_px=bx,b_y_px=by)); i+=1
    cap.release(); out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True)
    with out.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
    print(out)
if __name__=="__main__": main()
