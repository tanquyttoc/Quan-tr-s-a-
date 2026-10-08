import streamlit as st
from datetime import datetime
import uuid

# ============================================================
# CẤU HÌNH APP
# ============================================================

st.set_page_config(
    page_title="Trà Sữa POS",
    page_icon="🧋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CSS GIAO DIỆN
# ============================================================

st.markdown("""
<style>
    .main {
        background-color: #fff8fb;
    }

    .title {
        text-align: center;
        color: #d63384;
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #777;
        font-size: 17px;
        margin-bottom: 25px;
    }

    .product-card {
        background: white;
        padding: 18px;
        border-radius: 15px;
        box-shadow: 0 3px 12px rgba(0,0,0,0.08);
        margin-bottom: 15px;
    }

    .total-box {
        background: #ffe5f0;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin-top: 15px;
    }

    .total-price {
        color: #d63384;
        font-size: 32px;
        font-weight: 800;
    }

    .invoice {
        background: white;
        padding: 30px;
        border-radius: 15px;
        border: 1px solid #ddd;
        font-family: monospace;
    }

    div.stButton > button {
        border-radius: 10px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# DỮ LIỆU MENU
# ============================================================

MENU = {
    "Trà sữa truyền thống": 30000,
    "Trà sữa matcha": 35000,
    "Trà sữa socola": 35000,
    "Trà sữa khoai môn": 35000,
    "Trà sữa dâu": 35000,
    "Trà sữa thái xanh": 30000,
    "Trà sữa thái đỏ": 30000,
    "Trà đào": 30000,
    "Trà vải": 30000,
    "Trà chanh": 25000,
    "Matcha latte": 40000,
    "Cacao sữa": 35000
}

SIZES = {
    "S": 0,
    "M": 5000,
    "L": 10000
}

TOPPINGS = {
    "Không topping": 0,
    "Trân châu đen": 5000,
    "Trân châu trắng": 5000,
    "Thạch trái cây": 5000,
    "Thạch phô mai": 7000,
    "Pudding trứng": 7000,
    "Kem cheese": 10000,
    "Hạt thủy tinh": 6000
}

SUGAR_LEVELS = [
    "0% đường",
    "30% đường",
    "50% đường",
    "70% đường",
    "100% đường"
]

ICE_LEVELS = [
    "0% đá",
    "30% đá",
    "50% đá",
    "70% đá",
    "100% đá"
]


# ============================================================
# SESSION STATE
# ============================================================

if "cart" not in st.session_state:
    st.session_state.cart = []

if "invoice" not in st.session_state:
    st.session_state.invoice = None

if "customer_name" not in st.session_state:
    st.session_state.customer_name = ""


# ============================================================
# HÀM ĐỊNH DẠNG TIỀN
# ============================================================

def format_money(number):
    return f"{number:,.0f} VNĐ".replace(",", ".")


# ============================================================
# HÀM TẠO MÃ HÓA ĐƠN
# ============================================================

def create_invoice_code():
    now = datetime.now()
    random_part = str(uuid.uuid4())[:5].upper()
    return f"TS{now.strftime('%Y%m%d%H%M%S')}{random_part}"


# ============================================================
# HÀM TẠO NỘI DUNG HÓA ĐƠN
# ============================================================

def create_invoice_text(invoice):
    lines = []

    lines.append("=" * 50)
    lines.append("             TRÀ SỮA")
    lines.append("        HÓA ĐƠN THANH TOÁN")
    lines.append("=" * 50)

    lines.append(f"Mã hóa đơn : {invoice['code']}")
    lines.append(f"Thời gian   : {invoice['time']}")
    lines.append(f"Khách hàng  : {invoice['customer']}")
    lines.append("-" * 50)

    for index, item in enumerate(invoice["items"], 1):
        lines.append(
            f"{index}. {item['name']} - Size {item['size']}"
        )

        lines.append(
            f"   Topping: {item['topping']}"
        )

        lines.append(
            f"   Đường: {item['sugar']} | Đá: {item['ice']}"
        )

        lines.append(
            f"   SL: {item['quantity']} x "
            f"{format_money(item['unit_price'])}"
        )

        lines.append(
            f"   Thành tiền: {format_money(item['total'])}"
        )

        lines.append("-" * 50)

    lines.append(f"TỔNG TIỀN: {format_money(invoice['total'])}")
    lines.append("=" * 50)
    lines.append("       CẢM ƠN QUÝ KHÁCH!")
    lines.append("        HẸN GẶP LẠI ❤️")
    lines.append("=" * 50)

    return "\n".join(lines)


# ============================================================
# TIÊU ĐỀ
# ============================================================

st.markdown(
    '<div class="title">🧋 TRÀ SỮA POS</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Hệ thống bán hàng & quản lý hóa đơn</div>',
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("👤 Thông tin khách hàng")

    customer_name = st.text_input(
        "Tên khách hàng",
        value=st.session_state.customer_name,
        placeholder="Nhập tên khách hàng..."
    )

    st.session_state.customer_name = customer_name

    st.divider()

    st.header("🛒 Giỏ hàng")

    if len(st.session_state.cart) == 0:
        st.info("Chưa có món nào.")

    else:
        for i, item in enumerate(st.session_state.cart):

            st.write(
                f"**{i+1}. {item['name']}** "
                f"x{item['quantity']}"
            )

            st.caption(
                f"Size {item['size']} • "
                f"{format_money(item['total'])}"
            )

        cart_total = sum(
            item["total"]
            for item in st.session_state.cart
        )

        st.markdown("---")

        st.metric(
            "Tổng tiền",
            format_money(cart_total)
        )

        if st.button(
            "🗑️ Xóa toàn bộ giỏ hàng",
            use_container_width=True
        ):
            st.session_state.cart = []
            st.rerun()


# ============================================================
# KHU VỰC CHỌN MÓN
# ============================================================

st.subheader("🧋 Chọn món")

col1, col2 = st.columns(2)

with col1:

    drink = st.selectbox(
        "Loại đồ uống",
        list(MENU.keys())
    )

    size = st.radio(
        "Size",
        list(SIZES.keys()),
        horizontal=True
    )

    quantity = st.number_input(
        "Số lượng",
        min_value=1,
        max_value=50,
        value=1,
        step=1
    )

with col2:

    topping = st.selectbox(
        "Topping",
        list(TOPPINGS.keys())
    )

    sugar = st.selectbox(
        "Mức độ đường",
        SUGAR_LEVELS
    )

    ice = st.selectbox(
        "Mức độ đá",
        ICE_LEVELS
    )


# ============================================================
# TÍNH GIÁ
# ============================================================

base_price = MENU[drink]
size_price = SIZES[size]
topping_price = TOPPINGS[topping]

unit_price = (
    base_price
    + size_price
    + topping_price
)

total_price = unit_price * quantity


st.markdown(
    f"""
    <div class="total-box">
        <div>Đơn giá</div>
        <div class="total-price">
            {format_money(unit_price)}
        </div>
        <div>
            Số lượng: {quantity}
            &nbsp; | &nbsp;
            Thành tiền: <b>{format_money(total_price)}</b>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# THÊM MÓN
# ============================================================

st.write("")

if st.button(
    "➕ THÊM MÓN VÀO HÓA ĐƠN",
    type="primary",
    use_container_width=True
):

    new_item = {
        "name": drink,
        "size": size,
        "topping": topping,
        "sugar": sugar,
        "ice": ice,
        "quantity": quantity,
        "unit_price": unit_price,
        "total": total_price
    }

    st.session_state.cart.append(new_item)

    st.success(
        f"Đã thêm {quantity} x {drink} vào hóa đơn!"
    )

    st.rerun()


# ============================================================
# DANH SÁCH MÓN TRONG HÓA ĐƠN
# ============================================================

st.divider()

st.subheader("🛒 Chi tiết hóa đơn")

if not st.session_state.cart:

    st.info(
        "Hóa đơn đang trống. "
        "Hãy chọn món rồi bấm 'Thêm món vào hóa đơn'."
    )

else:

    for i, item in enumerate(st.session_state.cart):

        with st.container(border=True):

            c1, c2, c3, c4, c5 = st.columns(
                [0.5, 2.3, 1, 1, 1]
            )

            with c1:
                st.write(f"**{i+1}**")

            with c2:
                st.write(f"**{item['name']}**")
                st.caption(
                    f"Size {item['size']} | "
                    f"Topping: {item['topping']} | "
                    f"{item['sugar']} | {item['ice']}"
                )

            with c3:
                st.write(
                    f"SL: **{item['quantity']}**"
                )

            with c4:
                st.write(
                    format_money(item["unit_price"])
                )

            with c5:

                st.write(
                    format_money(item["total"])
                )

                if st.button(
                    "❌",
                    key=f"remove_{i}"
                ):
                    st.session_state.cart.pop(i)
                    st.rerun()


# ============================================================
# THANH TOÁN
# ============================================================

st.divider()

if st.session_state.cart:

    grand_total = sum(
        item["total"]
        for item in st.session_state.cart
    )

    left, right = st.columns([2, 1])

    with left:

        st.markdown(
            f"""
            <div class="total-box">
                <div>TỔNG THANH TOÁN</div>
                <div class="total-price">
                    {format_money(grand_total)}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with right:

        st.write("")

        if st.button(
            "💳 THANH TOÁN",
            type="primary",
            use_container_width=True
        ):

            if not customer_name.strip():
                st.warning(
                    "Vui lòng nhập tên khách hàng."
                )

            else:

                invoice = {
                    "code": create_invoice_code(),
                    "time": datetime.now().strftime(
                        "%d/%m/%Y %H:%M:%S"
                    ),
                    "customer": customer_name,
                    "items": st.session_state.cart.copy(),
                    "total": grand_total
                }

                st.session_state.invoice = invoice

                st.success(
                    "Thanh toán thành công!"
                )

                st.rerun()


# ============================================================
# HIỂN THỊ HÓA ĐƠN SAU KHI THANH TOÁN
# ============================================================

if st.session_state.invoice:

    invoice = st.session_state.invoice

    st.divider()

    st.subheader("🧾 HÓA ĐƠN ĐÃ THANH TOÁN")

    invoice_text = create_invoice_text(invoice)

    st.markdown(
        f"""
        <div class="invoice">

        <h2 style="text-align:center;">
        🧋 TRÀ SỮA
        </h2>

        <h3 style="text-align:center;">
        HÓA ĐƠN THANH TOÁN
        </h3>

        <hr>

        <b>Mã hóa đơn:</b> {invoice['code']}<br>
        <b>Thời gian:</b> {invoice['time']}<br>
        <b>Khách hàng:</b> {invoice['customer']}<br>

        <hr>
        """,
        unsafe_allow_html=True
    )

    for index, item in enumerate(
        invoice["items"], 1
    ):

        st.markdown(
            f"""
            <div class="product-card">

            <b>{index}. {item['name']}</b><br>

            Size: {item['size']}<br>
            Topping: {item['topping']}<br>
            Đường: {item['sugar']}<br>
            Đá: {item['ice']}<br>
            Số lượng: {item['quantity']}<br>

            Đơn giá:
            {format_money(item['unit_price'])}<br>

            <b>
            Thành tiền:
            {format_money(item['total'])}
            </b>

            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        f"""
        <div class="total-box">
            <div>TỔNG THANH TOÁN</div>
            <div class="total-price">
                {format_money(invoice['total'])}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <p style="text-align:center;">
        ❤️ Cảm ơn quý khách! Hẹn gặp lại!
        </p>
        """,
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # XUẤT HÓA ĐƠN
    # --------------------------------------------------------

    st.download_button(
        label="📥 XUẤT HÓA ĐƠN",
        data=invoice_text,
        file_name=f"{invoice['code']}.txt",
        mime="text/plain",
        use_container_width=True
    )

    # --------------------------------------------------------
    # ĐƠN HÀNG MỚI
    # --------------------------------------------------------

    if st.button(
        "🆕 TẠO HÓA ĐƠN MỚI",
        use_container_width=True
    ):

        st.session_state.cart = []
        st.session_state.invoice = None
        st.session_state.customer_name = ""

        st.rerun()
      
