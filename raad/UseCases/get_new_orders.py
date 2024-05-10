import mysql.connector
from django.conf import settings
from raad.models import ConfigModel


woocommerce_db_config = {
    "host": settings.WOOCOMMERCE_HOST,
    "port": 3306,
    "user": settings.WOOCOMMERCE_USER,
    "passwd": settings.WOOCOMMERCE_PASSWORD,
    "database": settings.WOOCOMMERCE_DB
}


LAST_ORDER_ID_CONFIG_KEY = "woocommerce_last_processed_order"
query_limit = 10


def get_last_order_id():
    try:
        config = ConfigModel.objects.get(key=LAST_ORDER_ID_CONFIG_KEY)
    except ConfigModel.DoesNotExist:
        config = ConfigModel.objects.create(
            key=LAST_ORDER_ID_CONFIG_KEY,
            value='0'
        )
    return int(config.value)


def save_last_order_id(order_id):
    try:
        config = ConfigModel.objects.get(key=LAST_ORDER_ID_CONFIG_KEY)
        config.value = str(order_id)
        config.save()
    except ConfigModel.DoesNotExist:
        ConfigModel.objects.create(
            key=LAST_ORDER_ID_CONFIG_KEY,
            value=str(order_id)
        )


def get_new_orders():
    connection = mysql.connector.connect(**woocommerce_db_config)
    cursor = connection.cursor()

    last_order_id = get_last_order_id()

    cursor.execute(f"SELECT * FROM wp_posts WHERE post_type = 'shop_order' AND post_status = 'wc-completed' AND ID > {last_order_id} LIMIT {query_limit};")
    orders = cursor.fetchall()

    order_data = []

    for order in orders:
        order_id = order[0]

        cursor.execute(f"SELECT meta_value FROM wp_postmeta WHERE post_id = {order_id} AND meta_key = '_billing_phone';")
        user_phone = cursor.fetchone()
        phone = user_phone[0] if user_phone else None

        cursor.execute(f"SELECT meta_value FROM wp_postmeta WHERE post_id = {order_id} AND meta_key = '_billing_email';")
        user_email = cursor.fetchone()
        email = user_email[0] if user_email else None

        cursor.execute(
            f"SELECT * FROM wp_woocommerce_order_items join "
            f"wp_woocommerce_order_itemmeta wwoi on wp_woocommerce_order_items.order_item_id = wwoi.order_item_id "
            f"WHERE order_id =  {order_id} AND meta_key = '_product_id';")
        order_items = cursor.fetchall()

        formatted_order_items = []

        for item in order_items:
            cursor.execute(f"SELECT meta_value FROM wp_woocommerce_order_itemmeta WHERE order_item_id = {item[0]} AND meta_key = '_qty';")
            qty = cursor.fetchone()[0]

            formatted_order_items.append({
                "order_item_id": item[0],
                "qty": qty,
                "product_id": int(item[7]),
            })

        order_data.append({
            "order_id": order_id,
            "order_user_phone": phone,
            "order_user_email": email,
            "items": formatted_order_items
        })

        save_last_order_id(order_id)

    cursor.close()
    connection.close()

    return order_data
