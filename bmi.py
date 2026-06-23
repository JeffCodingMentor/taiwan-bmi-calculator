import streamlit as st

# --- PAGE SETUP ---
st.set_page_config(
    page_title="臺灣兒童與成人 BMI 健康計算機",
    page_icon="⚖️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- CHILD BMI LOOKUP TABLE (Taiwan Ministry of Health and Welfare) ---
# Format: age: { "boy": (normal_min, overweight_min, obese_min), "girl": (normal_min, overweight_min, obese_min) }
# Source: 衛生福利部國民健康署 兒童及青少年生長身體質量指數(BMI)建議值
CHILD_BMI_TABLE = {
    2:  {"boy": (14.2, 17.4, 18.3), "girl": (13.7, 17.2, 18.1)},
    3:  {"boy": (13.7, 17.0, 17.8), "girl": (13.5, 16.9, 17.8)},
    4:  {"boy": (13.4, 16.7, 17.6), "girl": (13.2, 16.8, 17.9)},
    5:  {"boy": (13.3, 16.7, 17.7), "girl": (13.1, 17.0, 18.1)},
    6:  {"boy": (13.5, 16.9, 18.5), "girl": (13.1, 17.2, 18.8)},
    7:  {"boy": (13.8, 17.9, 20.3), "girl": (13.4, 17.7, 19.6)},
    8:  {"boy": (14.1, 19.0, 21.6), "girl": (13.8, 18.4, 20.7)},
    9:  {"boy": (14.3, 19.5, 22.3), "girl": (14.0, 19.1, 21.3)},
    10: {"boy": (14.5, 20.0, 22.7), "girl": (14.3, 19.7, 22.0)},
    11: {"boy": (14.8, 20.7, 23.2), "girl": (14.7, 20.5, 22.7)},
    12: {"boy": (15.2, 21.3, 23.9), "girl": (15.2, 21.3, 23.5)},
    13: {"boy": (15.7, 21.9, 24.5), "girl": (15.7, 21.9, 24.3)},
    14: {"boy": (16.3, 22.5, 25.1), "girl": (16.1, 22.3, 24.9)},
    15: {"boy": (16.9, 22.9, 25.4), "girl": (16.7, 22.7, 25.2)},
    16: {"boy": (17.4, 23.3, 25.6), "girl": (17.2, 22.7, 25.3)},
    17: {"boy": (17.8, 23.5, 25.6), "girl": (17.3, 22.7, 25.3)}
}

# --- CUSTOM CSS (Premium UI with Glassmorphism & Sleek Design) ---
st.markdown("""
<style>
    /* Gradient Title */
    .title-gradient {
        font-weight: 800;
        background: linear-gradient(135deg, #10b981 0%, #3b82f6 50%, #6366f1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.6rem;
        margin-bottom: 0.2rem;
        text-align: center;
    }
    
    .subtitle-text {
        color: #94a3b8;
        font-size: 1.1rem;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Premium glassmorphism card */
    .result-card {
        background: rgba(30, 41, 59, 0.45);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -2px rgba(0, 0, 0, 0.02);
        margin-top: 1.5rem;
        margin-bottom: 1.5rem;
        color: #f8fafc;
    }
    
    .metric-title {
        font-size: 0.95rem;
        color: #94a3b8;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .metric-value {
        font-size: 3.5rem;
        font-weight: 800;
        line-height: 1.1;
    }
    
    .status-badge {
        display: inline-block;
        padding: 6px 16px;
        border-radius: 9999px;
        font-weight: 700;
        font-size: 1.1rem;
        color: white;
        margin-top: 8px;
    }
    
    .info-card {
        background-color: rgba(15, 23, 42, 0.4);
        border-left: 4px solid #3b82f6;
        padding: 12px 16px;
        border-radius: 0 8px 8px 0;
        margin-bottom: 12px;
        color: #f8fafc;
    }
</style>
""", unsafe_allow_html=True)

# --- HEADER SECTION ---
st.markdown('<div class="title-gradient">⚖️ 臺灣兒童與成人 BMI 健康計算機</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-text">依據中華民國衛生福利部國民健康署最新體位標準設計</div>', unsafe_allow_html=True)

# --- INPUT SECTION CONTAINER ---
with st.container(border=True):
    st.markdown("### 📋 輸入基本資料")
    
    # 1. Age Group Selector
    age_group = st.radio(
        "年齡類別",
        options=["18 歲以上成人", "未滿 18 歲兒童與青少年"],
        horizontal=True,
        help="衛福部之青少年及兒童與成人的體位標準與計算判定機制不同，請正確選擇。"
    )
    
    st.markdown("<hr style='margin: 10px 0;'>", unsafe_allow_html=True)
    
    # 2. Dynamically Render Columns based on Age Group
    if age_group == "18 歲以上成人":
        col1, col2, col3 = st.columns(3)
        with col1:
            gender = st.radio("性別", options=["男 ♂️", "女 ♀️"], horizontal=True, help="男性與女性的健康腰圍標準不同。")
            age = 18  # Default adult age
        with col2:
            height = st.number_input("身高 (cm)", min_value=50.0, max_value=250.0, value=170.0, step=0.5, format="%.1f")
        with col3:
            weight = st.number_input("體重 (kg)", min_value=10.0, max_value=300.0, value=65.0, step=0.5, format="%.1f")
    else:
        col1, col2, col3, col4 = st.columns([1.2, 1, 1, 1])
        with col1:
            gender = st.radio("生理性別", options=["男 ♂️", "女 ♀️"], horizontal=True, help="發育期男童與女童之 BMI 標準有所差異。")
        with col2:
            age = st.selectbox("足歲年齡 (歲)", options=list(range(2, 18)), index=10, help="請選擇孩子目前的足歲年齡（2~17 歲）。")
        with col3:
            height = st.number_input("身高 (cm)", min_value=50.0, max_value=250.0, value=150.0, step=0.5, format="%.1f")
        with col4:
            weight = st.number_input("體重 (kg)", min_value=5.0, max_value=300.0, value=40.0, step=0.5, format="%.1f")

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    calculate_btn = st.button("⚖️ 開始計算 BMI", type="primary", use_container_width=True)

# --- INITIALIZE SESSION STATE FOR PERSISTENCE ---
if "calculated" not in st.session_state:
    st.session_state.calculated = False
if "age_group" not in st.session_state:
    st.session_state.age_group = "18 歲以上成人"
if "gender" not in st.session_state:
    st.session_state.gender = "男 ♂️"
if "age" not in st.session_state:
    st.session_state.age = 18
if "height" not in st.session_state:
    st.session_state.height = 170.0
if "weight" not in st.session_state:
    st.session_state.weight = 65.0

# --- WHEN BUTTON PRESSED ---
if calculate_btn:
    st.session_state.calculated = True
    st.session_state.age_group = age_group
    st.session_state.gender = gender
    st.session_state.height = height
    st.session_state.weight = weight
    st.session_state.age = age

# --- RESULTS AREA ---
if st.session_state.calculated:
    ag = st.session_state.age_group
    g = st.session_state.gender
    h = st.session_state.height
    w = st.session_state.weight
    curr_age = st.session_state.age
    
    # Calculate BMI
    height_m = h / 100.0
    bmi = w / (height_m ** 2)
    
    # Prepare Display Variables
    status = ""
    color = ""
    suggestion = ""
    alert_type = "info"
    
    if ag == "18 歲以上成人":
        # Healthy Weight Range (Adult)
        min_healthy = 18.5 * (height_m ** 2)
        max_healthy = 24.0 * (height_m ** 2)
        
        # Adult standard mapping
        if bmi < 18.5:
            status = "體重過輕"
            color = "#38bdf8"  # Sky blue
            alert_type = "info"
            suggestion = "您的體格偏瘦，可能存在營養不均、骨質疏鬆或免疫力下降等健康風險。建議增加優質蛋白質（如蛋、奶、豆類、瘦肉）與健康脂肪的攝取，並搭配規律的重量訓練（肌力訓練）來刺激肌肉增長。若長期無法增重，建議諮詢家醫科醫師或營養師以獲得專業評估。"
        elif 18.5 <= bmi < 24:
            status = "健康體重"
            color = "#10b981"  # Green
            alert_type = "success"
            suggestion = "非常恭喜！您的體重完全在衛福部推薦的健康標準範圍內。這能顯著降低代謝症候群、心血管疾病與第二型糖尿病的患病風險。請繼續維持均衡的「三低一高」（低油、低糖、低鹽及高纖）飲食結構，並維持規律的生活作息與適度運動。"
        elif 24 <= bmi < 27:
            status = "體重過重"
            color = "#fbbf24"  # Amber
            alert_type = "warning"
            suggestion = "您的體重已進入過重區間，代表心血管與代謝系統開始面臨額外的負擔。建議開始進行溫和的健康體重管理：減少精緻澱粉、油炸物及含糖飲料的攝取，增加日常步行及中等強度有氧運動的頻率（每週至少 150 分鐘，如快走、自行車），避免體重進一步上升。"
        elif 27 <= bmi < 30:
            status = "輕度肥胖"
            color = "#f97316"  # Orange
            alert_type = "warning"
            suggestion = "您的體位已符合輕度肥胖標準。肥胖已被醫學界定義為一種慢性病，易引發高血壓、高血脂及脂肪肝等問題。強烈建議重新檢視飲食習慣，實行總熱量控制，並採取有氧運動與阻力運動並重的運動計劃，以提高基礎代謝率並燃燒多餘體脂肪。"
        elif 30 <= bmi < 35:
            status = "中度肥胖"
            color = "#ef4444"  # Red
            alert_type = "error"
            suggestion = "您的 BMI 落在中度肥胖區間，這顯著增加了動脈硬化、中風、高血壓及關節退化的機率。建議尋求專業營養師或醫療門診（如減重門診、新陳代謝科）指導，規劃安全性高且可持續的飲食控制與減重計劃。運動時請著重保護膝關節，避免高衝擊性運動。"
        else:  # bmi >= 35
            status = "重度肥胖"
            color = "#7f1d1d"  # Dark Red
            alert_type = "error"
            suggestion = "您處於重度肥胖狀態，伴隨重度脂肪肝、心血管疾病、呼吸睡眠中止症及關節退化等併發症之風險極高。強烈建議前往醫院的「體重管理專科門診（減重門診）」進行全面的健康與代謝檢查。透過專業醫療團隊（醫師、營養師、物理治療師）的共同照護，以最安全、科學的方式重建健康體格。"
            
        # Adult Gauge HTML
        # Map BMI to percentage using piecewise linear interpolation (6 equal blocks)
        def get_adult_percentage(b):
            val_clamped = max(10.0, min(40.0, b))
            points = [
                (10.0, 0.0),
                (18.5, 16.67),
                (24.0, 33.33),
                (27.0, 50.0),
                (30.0, 66.67),
                (35.0, 83.33),
                (40.0, 100.0)
            ]
            for idx in range(len(points) - 1):
                x1, y1 = points[idx]
                x2, y2 = points[idx+1]
                if x1 <= val_clamped <= x2:
                    return y1 + (val_clamped - x1) * (y2 - y1) / (x2 - x1)
            return 100.0

        percentage = get_adult_percentage(bmi)
        
        gauge_html = f"""
        <div style="margin: 25px 0 10px 0;">
            <div style="font-weight: 600; font-size: 0.95rem; color: #94a3b8; margin-bottom: 8px;">📊 臺灣成人 BMI 分級圖表定位</div>
            <div style="display: flex; height: 38px; border-radius: 8px; overflow: hidden; font-weight: bold; font-size: 10px; color: white; text-shadow: 1px 1px 1px rgba(0,0,0,0.2); line-height: 1.2;">
                <div style="flex: 1; background: #38bdf8; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 2px;">
                    <span>過輕</span><span style="font-size: 9px; font-weight: normal; opacity: 0.95;">&lt;18.5</span>
                </div>
                <div style="flex: 1; background: #10b981; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 2px;">
                    <span>正常</span><span style="font-size: 9px; font-weight: normal; opacity: 0.95;">18.5-24</span>
                </div>
                <div style="flex: 1; background: #fbbf24; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 2px;">
                    <span>過重</span><span style="font-size: 9px; font-weight: normal; opacity: 0.95;">24-27</span>
                </div>
                <div style="flex: 1; background: #f97316; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 2px;">
                    <span>輕度肥胖</span><span style="font-size: 9px; font-weight: normal; opacity: 0.95;">27-30</span>
                </div>
                <div style="flex: 1; background: #ef4444; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 2px;">
                    <span>中度肥胖</span><span style="font-size: 9px; font-weight: normal; opacity: 0.95;">30-35</span>
                </div>
                <div style="flex: 1; background: #7f1d1d; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 2px;">
                    <span>重度肥胖</span><span style="font-size: 9px; font-weight: normal; opacity: 0.95;">&ge;35</span>
                </div>
            </div>
            <div style="position: relative; width: 100%; height: 32px;">
                <div style="position: absolute; left: calc({percentage}% - 8px); top: 2px; transition: left 0.6s ease-in-out; display: flex; flex-direction: column; align-items: center;">
                    <div style="width: 0; height: 0; border-left: 8px solid transparent; border-right: 8px solid transparent; border-bottom: 8px solid #374151;"></div>
                    <div style="background-color: #374151; color: white; font-size: 11px; padding: 3px 8px; border-radius: 6px; font-weight: 700; white-space: nowrap; margin-top: 1px; box-shadow: 0 2px 4px rgba(0,0,0,0.15);">
                        您的 BMI: {bmi:.2f}
                    </div>
                </div>
            </div>
        </div>
        """
    else:
        # Retrieve Child Thresholds
        gender_key = "boy" if "男" in g else "girl"
        thresholds = CHILD_BMI_TABLE[curr_age][gender_key]
        normal_min, overweight_min, obese_min = thresholds
        
        # Healthy Weight Range (Child)
        min_healthy = normal_min * (height_m ** 2)
        max_healthy = overweight_min * (height_m ** 2)
        
        # Child status mapping
        if bmi < normal_min:
            status = "體重過輕"
            color = "#38bdf8"
            alert_type = "info"
            suggestion = f"孩子的體格偏瘦（BMI 低於該年齡標準 {normal_min}）。兒童與青少年正處於生長發育的關鍵期，體重過輕可能導致發育遲緩、免疫力低或骨骼結構不健全。建議確保孩子獲得均衡且足量的六大類食物，適度補充足量蛋白質與熱量，並維持每天充足睡眠。若生長發育長期落後，建議諮詢小兒科醫師進行健康評估。"
        elif normal_min <= bmi < overweight_min:
            status = "健康體位"
            color = "#10b981"
            alert_type = "success"
            suggestion = f"非常棒！孩子的體格處於健康體位（BMI 介於 {normal_min} ~ {overweight_min} 之間），這是在衛福部理想的生長曲線範圍內。請繼續鼓勵孩子多吃新鮮天然食材、多喝白開水（避免含糖飲料與高油零食），並養成每天累計 60 分鐘以上中高強度運動（如跳繩、球類、跑步）的習慣以強壯體格。"
        elif overweight_min <= bmi < obese_min:
            status = "體重過重"
            color = "#fbbf24"
            alert_type = "warning"
            suggestion = f"孩子的體重偏重（BMI 超過過重門檻 {overweight_min}）。這階段不建議盲目幫孩子限制卡路里或進行劇烈節食，以免阻礙發育。建議採取「調整生活型態」：減少油炸食品、零食及含甜飲料，每日均衡攝取多色蔬菜與水果，並限制看電視、玩手遊等久坐時間，多去戶外進行親子運動。"
        else: # bmi >= obese_min
            status = "肥胖"
            color = "#ef4444"
            alert_type = "error"
            suggestion = f"孩子的 BMI 已達到肥胖標準（BMI ≧ {obese_min}）。兒童肥胖容易延續至成年，並顯著提升日後罹患糖尿病、三高與脂肪肝的風險。強烈建議尋求兒童內分泌科、小兒科醫師或專業兒童營養師協助，進行完整的健康與代謝檢查。在家中請建立「全家共同參與」的飲食計畫，切勿孤立或責怪孩子，以溫和且科學的陪伴引導孩子恢復健康體態。"
            
        # Child Gauge HTML
        # Map child BMI to percentage using piecewise linear interpolation (4 equal blocks)
        def get_child_percentage(b, n_min, ow_min, ob_min):
            b0 = n_min - 4.0
            b1 = n_min
            b2 = ow_min
            b3 = ob_min
            b4 = ob_min + 5.0
            val_clamped = max(b0, min(b4, b))
            
            points = [
                (b0, 0.0),
                (b1, 25.0),
                (b2, 50.0),
                (b3, 75.0),
                (b4, 100.0)
            ]
            for idx in range(len(points) - 1):
                x1, y1 = points[idx]
                x2, y2 = points[idx+1]
                if x1 <= val_clamped <= x2:
                    return y1 + (val_clamped - x1) * (y2 - y1) / (x2 - x1)
            return 100.0

        percentage = get_child_percentage(bmi, normal_min, overweight_min, obese_min)
        
        gauge_html = f"""
        <div style="margin: 25px 0 10px 0;">
            <div style="font-weight: 600; font-size: 0.95rem; color: #94a3b8; margin-bottom: 8px;">📊 臺灣兒童/青少年 ({curr_age}歲{g[0]}生) BMI 分級圖表定位</div>
            <div style="display: flex; height: 38px; border-radius: 8px; overflow: hidden; font-weight: bold; font-size: 10px; color: white; text-shadow: 1px 1px 1px rgba(0,0,0,0.2); line-height: 1.2;">
                <div style="flex: 1; background: #38bdf8; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 2px;">
                    <span>過輕</span><span style="font-size: 9px; font-weight: normal; opacity: 0.95;">&lt;{normal_min:.1f}</span>
                </div>
                <div style="flex: 1; background: #10b981; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 2px;">
                    <span>健康體位</span><span style="font-size: 9px; font-weight: normal; opacity: 0.95;">{normal_min:.1f}-{overweight_min:.1f}</span>
                </div>
                <div style="flex: 1; background: #fbbf24; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 2px;">
                    <span>過重</span><span style="font-size: 9px; font-weight: normal; opacity: 0.95;">{overweight_min:.1f}-{obese_min:.1f}</span>
                </div>
                <div style="flex: 1; background: #ef4444; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 2px;">
                    <span>肥胖</span><span style="font-size: 9px; font-weight: normal; opacity: 0.95;">&ge;{obese_min:.1f}</span>
                </div>
            </div>
            <div style="position: relative; width: 100%; height: 32px;">
                <div style="position: absolute; left: calc({percentage}% - 8px); top: 2px; transition: left 0.6s ease-in-out; display: flex; flex-direction: column; align-items: center;">
                    <div style="width: 0; height: 0; border-left: 8px solid transparent; border-right: 8px solid transparent; border-bottom: 8px solid #374151;"></div>
                    <div style="background-color: #374151; color: white; font-size: 11px; padding: 3px 8px; border-radius: 6px; font-weight: 700; white-space: nowrap; margin-top: 1px; box-shadow: 0 2px 4px rgba(0,0,0,0.15);">
                        您的 BMI: {bmi:.2f}
                    </div>
                </div>
            </div>
        </div>
        """

    # Render results in columns
    st.markdown("### 📊 計算結果")
    
    # Custom styled container for results
    st.markdown(f"""
    <div class="result-card">
        <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center;">
            <div>
                <span class="metric-title">計算所得之身體質量指數 (BMI)</span>
                <div class="metric-value" style="color: {color};">{bmi:.2f}</div>
                <span class="status-badge" style="background-color: {color};">{status}</span>
            </div>
            <div style="flex-grow: 1; max-width: 420px; margin-top: 15px; min-width: 250px;">
                <div class="info-card" style="border-left-color: {color};">
                    <strong>📏 身高符合之健康體重區間：</strong><br>
                    <span style="font-size: 1.1rem; color: #f8fafc; font-weight: 600;">{min_healthy:.1f} kg ~ {max_healthy:.1f} kg</span>
                </div>
                <div class="info-card" style="border-left-color: #6366f1; margin-bottom: 0;">
                    <strong>💡 健康指引提醒：</strong><br>
                    {"男性腰圍應控制於 <b>90 公分</b>以下" if (ag == "18 歲以上成人" and "男" in g) else 
                     ("女性腰圍應控制於 <b>80 公分</b>以下" if (ag == "18 歲以上成人" and "女" in g) else 
                      "腰圍標準僅適用成人，發育期兒童青少年以 <b>BMI 對照</b>為主")}
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Render interactive gauge bar
    st.markdown(gauge_html, unsafe_allow_html=True)
    
    # Render customized recommendation
    st.markdown("### 💡 專屬健康建議與指引")
    if alert_type == "success":
        st.success(suggestion)
    elif alert_type == "info":
        st.info(suggestion)
    elif alert_type == "warning":
        st.warning(suggestion)
    else:
        st.error(suggestion)
        
    # Standard warning context
    st.caption(f"⚠️ 本評估係依據衛福部國民健康署公佈之{'「18歲以上成人體位標準」' if ag == '18 歲以上成人' else '「兒童及青少年生長身體質量指數建議值」'}進行判讀。體重與發育涉及個體基因與多項生理特徵，若有成長發育或減重之疑慮，請務必尋求合格醫療團隊進行專業評估與指導。")
