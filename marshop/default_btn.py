from aiogram.types import ReplyKeyboardMarkup,KeyboardButton

phone_number = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Share Contact",request_contact=True)
        ]
    ],resize_keyboard=True
)


shop_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("My Order"),
            KeyboardButton("MARS Shop"),
        ],
        [
            KeyboardButton("My Products"),
            KeyboardButton("Profile"),
        ]
    ],resize_keyboard=True
)


my_product= ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Add Product"),
            KeyboardButton("Show Product"),
        ],
        [
            KeyboardButton("Back to")
        ]
    ],resize_keyboard=True
)






