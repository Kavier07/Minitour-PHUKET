from flask import Flask, render_template
import folium

app = Flask(__name__)

# ข้อมูลเส้นทางท่องเที่ยว Phuket One-Day Tour
LOCATIONS = [
    {
        "id": 1,
        "name": "Connext Condominium",
        "category": "ที่พัก (Basecamp)",
        "coords": [7.873739633922723, 98.38447908906252],
        "desc": "จุดเริ่มต้นการเดินทาง พักผ่อนสบายๆ ในบรรยากาศส่วนตัวใจกลางเมืองภูเก็ต พร้อมต้อนรับอรุณวันใหม่",
        "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQWLD5ZUAh1zMpSF2rAVzBj03QuTNRX7WBlp4ns8vCAIQ&s=10",
        "gmaps_link": "https://www.google.com/maps/dir/?api=1&destination=7.873739633922723,98.38447908906252"
    },
    {
        "id": 2,
        "name": "วงเวียนสะพานหิน",
        "category": "จุดเช็คอิน (Landmark)",
        "coords": [7.868611535300862, 98.39595781273218],
        "desc": "อนุสาวรีย์หลัก 60 ปี สัญลักษณ์สำคัญทางประวัติศาสตร์ยุคเหมืองแร่ดีบุกของเมืองภูเก็ต",
        "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSH3mIdqJH9qLmC34-FmUxvTty2YoN8Lil1ogtUouWKiQ&s=10",
        "gmaps_link": "https://www.google.com/maps/dir/?api=1&destination=7.868611535300862,98.39595781273218"
    },
    {
        "id": 3,
        "name": "ริมหาดสะพานหิน",
        "category": "จุดท่องเที่ยว (Coastal View)",
        "coords": [7.867180013958043, 98.39943815602832],
        "desc": "สัมผัสสายลมทะเลชายหาดฝั่งเมือง จุดพักผ่อนเพื่อการผ่อนคลายและซึมซับวิถีชีวิตท้องถิ่น",
        "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSRfQgXTXHokwaV0SULjar3AVSAfg4tNVAY-xHOANFJuQ&s=10",
        "gmaps_link": "https://www.google.com/maps/dir/?api=1&destination=7.867180013958043,98.39943815602832"
    },
    {
        "id": 4,
        "name": "Summer liveaboard",
        "category": "จุดดำน้ำ (Diving & Adventure)",
        "coords": [7.871581779996354, 98.41446799188898],
        "desc": "ออกเดินทางสู่โลกใต้ท้องทะเลอันดามัน สัมผัสประสบการณ์ดำน้ำแบบพรีเมียม",
        "image": "https://lh3.googleusercontent.com/grass-cs/ACvplmMY2LIJY-bPTfwnJ9asdYgKkb3zCV8aDHfcp5YIL6INYUNbNLoDT1O9NRJsTok9Utv2miJCvspFom1oXO0bTj4Hf6cKexq0PUQ44n0qTBToAOBG7UIrqHkXgjHQXlXauPTv1TH_Uc9x3RgV=w326-h312-n-k-no",
        "gmaps_link": "https://www.google.com/maps/dir/?api=1&destination=7.871581779996354,98.41446799188898"
    },
    {
        "id": 5,
        "name": "พระธาตุอินทร์แขวนจำลอง",
        "category": "ไหว้พระ (Spiritual Heritage)",
        "coords": [7.880433442767307, 98.42597117039772],
        "desc": "กราบสักการะสิ่งศักดิ์สิทธิ์บนยอดเขา เสริมสิริมงคลพร้อมดื่มด่ำกับทัศนียภาพมุมสูง",
        "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS_NH8KB7y9-gK7t26QVn34SIR1vD9DSHDe1UhvhRECIA&s=10",
        "gmaps_link": "https://www.google.com/maps/dir/?api=1&destination=7.880433442767307,98.42597117039772"
    },
    {
        "id": 6,
        "name": "MOONSTo̲̲NE cafe over the Sea",
        "category": "คาเฟ่ (Cafe & Relax)",
        "coords": [7.829332817010188, 98.40617621180786],
        "desc": "จิบกาแฟริมผืนน้ำในดีไซน์มินิมอล เคลือบกลิ่นอายวินเทจ ปิดท้ายทริปอย่างสมบูรณ์แบบ",
        "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSEXRH4xYkiVX3EOf68Ab5QsViezqZb7L7cDEdrYpG3nQ&s=10",
        "gmaps_link": "https://www.google.com/maps/dir/?api=1&destination=7.829332817010188,98.40617621180786"
    }
]

def create_map():
    # พิกัดจุดกลางสำหรับแสดงผลแผนที่ initial view
    center_lat = 7.865
    center_lng = 98.405
    
    # เลือกใช้ CartoDB Positron โทนสว่าง มินิมอล เข้ากับสไตล์เว็บ
    m = folium.Map(
        location=[center_lat, center_lng],
        zoom_start=13,
        tiles="CartoDB positron",
        control_scale=True
    )
    
    # วาดเส้นทางการเดินทาง (Polyline) เชื่อม 6 จุด
    route_coords = [loc["coords"] for loc in LOCATIONS]
    folium.PolyLine(
        locations=route_coords,
        color="#2C2A29",
        weight=2.5,
        opacity=0.7,
        dash_array="6, 6"
    ).add_to(m)

    # เพิ่ม Custom Marker แต่ละสถานที่
    for loc in LOCATIONS:
        popup_content = f"""
        <div style="font-family: 'Playfair Display', 'Sarabun', serif; width: 190px; padding: 2px;">
            <img src="{loc['image']}" style="width:100%; height:100px; object-fit:cover; border-radius:2px; margin-bottom:8px;">
            <span style="font-size:10px; letter-spacing:1px; text-transform:uppercase; color:#8C8275; display:block;">Stop 0{loc['id']}</span>
            <h4 style="margin:2px 0 6px 0; font-size:13px; font-weight:600; color:#1A1918;">{loc['name']}</h4>
            <a href="{loc['gmaps_link']}" target="_blank" style="display:inline-block; font-size:11px; color:#1A1918; text-decoration:none; border-bottom:1px solid #1A1918;">นำทางใน Google Maps &rarr;</a>
        </div>
        """
        
        folium.Marker(
            location=loc["coords"],
            popup=folium.Popup(popup_content, max_width=220),
            tooltip=f"0{loc['id']}. {loc['name']}",
            icon=folium.DivIcon(
                html=f"""
                <div style="
                    background-color: #1C1B1A;
                    color: #F7F4EF;
                    border: 1px solid #C5A059;
                    border-radius: 50%;
                    width: 28px;
                    height: 28px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 11px;
                    font-family: serif;
                    font-weight: bold;
                    box-shadow: 0 4px 10px rgba(0,0,0,0.15);
                ">{loc['id']}</div>
                """
            )
        ).add_to(m)

    return m._repr_html_()

@app.route("/")
def index():
    map_html = create_map()
    return render_template("index.html", locations=LOCATIONS, map_html=map_html)

if __name__ == "__main__":
    app.run(debug=True)