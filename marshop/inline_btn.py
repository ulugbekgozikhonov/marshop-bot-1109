from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

product_button= InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("Edit product", callback_data="edit-product"),
            InlineKeyboardButton("Delete product", callback_data="delete-product")
        ], 
        [
            InlineKeyboardButton("Add to shop", callback_data="add-to-shop")
        ]
    ]
)



def show_product_btn(count):
    result = InlineKeyboardMarkup(row_width=3)
    
    for i in range(count):
        btn = InlineKeyboardButton(text=f"{i+1}",callback_data=f"btn_{i+1}")
        
        if i%2 == 0:
            result.add(btn)     
        else:
            result.insert(btn)
            
        

    old = InlineKeyboardButton("⬅️",callback_data="orqaga")
    delete = InlineKeyboardButton("❌",callback_data="delete")
    next = InlineKeyboardButton("➡️",callback_data="oldinga")
    
    result.add(old,delete,next)
    
    return result