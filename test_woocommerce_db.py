import mysql.connector


woocommerce_db_config = {
    "host": "",
    "port": 0,
    "user": "",
    "passwd": "",
    "database": ""
}



def get_new_orders():
    connection = mysql.connector.connect(**woocommerce_db_config)
    cursor = connection.cursor()

    last_order_id = 104

    cursor.execute(f"SELECT * FROM wp_posts WHERE post_type = 'shop_order' AND post_status = 'wc-completed' AND ID > {last_order_id} LIMIT {10};")
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
                "product_id": item[7],
            })

        order_data.append({
            "order_id": order_id,
            "order_user_phone": phone,
            "order_user_email": email,
            "items": formatted_order_items
        })

    cursor.close()
    connection.close()

    return order_data


print(get_new_orders())
