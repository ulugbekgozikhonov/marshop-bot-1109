from aiogram import Bot,Dispatcher,executor,types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
import logging

from default_btn import *
logging.basicConfig(level=logging.INFO)

from state import *
from database import DatabaseManager

BOT_TOKEN = "6835217351:AAF_0A6xl_Ag2S3jA4byQo8-J18s3BQCT8k"

bot = Bot(token=BOT_TOKEN,parse_mode="HTML")
storage = MemoryStorage()
dp = Dispatcher(bot=bot,storage=storage)

database = DatabaseManager("marshop.db")
async def on_startup(dp):
    database.create_tables()
    await bot.send_message(chat_id=909437832,text="Bot has started")

async def on_shutdown(dp):
    await bot.send_message(chat_id=909437832,text="Bot has stopped")

@dp.message_handler(commands="start")
async def start_handler(message:types.Message,state:FSMContext):
    chat_id = message.chat.id
    user = database.get_user_by_chat_id(chat_id=chat_id)
    if user:
        await message.answer(f"Welcome to MARS SHOP. Dear {user[2]}",reply_markup=shop_menu)
    else:
        await state.update_data(chat_id=chat_id)
        await message.answer("Welcome to MARS SHOP")
        await message.answer("You can register to use this bot:\n<b>Enter name</b>")
        await RegisterState.full_name.set()

@dp.message_handler(state=RegisterState.full_name)
async def ful_name_handler(message:types.Message,state:FSMContext):
    full_name = message.text
    await state.update_data(full_name=full_name)
    await message.answer("Share Contact",reply_markup=phone_number)
    await RegisterState.phone_number.set()

@dp.message_handler(state=RegisterState.phone_number,content_types=types.ContentType.CONTACT)
async def contact_handler(message:types.Message,state:FSMContext):
    phone_number = message.contact.phone_number
    await state.update_data(phone_number=phone_number)
    await message.answer("Successfully registred and you can use bot",reply_markup=shop_menu)
    data = await state.get_data()
    database.add_user(data=data)
    await state.finish()



@dp.message_handler(text="My Products")
async def my_product_handler(message:types.Message):
  await message.answer("Choice comand ",reply_markup=my_product)
  
  
@dp.message_handler(text="Add Product")
async def add_product_name_handler(message:types.Message):
    await message.answer("Enter product name:")
    await AddProductState.name.set()


@dp.message_handler(state=AddProductState.name)
async def add_product_name_handler(message:types.Message,state:FSMContext):
    paroduct_name = message.text
    await state.update_data(name=paroduct_name) 
    await message.answer("Send product photo:")
    await AddProductState.photo.set()

@dp.message_handler(state=AddProductState.photo,content_types="photo")
async def add_product_photo_handler(message:types.Message,state:FSMContext):
    paroduct_photo = message.photo[-1].file_id
    await state.update_data(photo=paroduct_photo) 
    await message.answer("Enter product price:")
    await AddProductState.price.set()

@dp.message_handler(state=AddProductState.price)
async def add_product_name_handler(message:types.Message,state:FSMContext):
    paroduct_price = message.text
    await state.update_data(price=paroduct_price) 
    await message.answer("Enter count:")
    await AddProductState.count.set()

@dp.message_handler(state=AddProductState.count)
async def add_product_name_handler(message:types.Message,state:FSMContext):
    paroduct_count = message.text
    await state.update_data(count=paroduct_count) 
    await message.answer("Enter product description:")
    await AddProductState.desc.set()

@dp.message_handler(state=AddProductState.desc)
async def add_product_name_handler(message:types.Message,state:FSMContext):
    paroduct_desc = message.text
    await state.update_data(description=paroduct_desc) 
    data = await state.get_data()
    chat_id = message.chat.id
    data["chat_id"] = chat_id
    print(data)
    if database.create_prodcut(data=data):
        await message.answer("Successfully created")
    else:
        await message.answer("Prodcut create error!!!!")
    await state.finish()
    
@dp.message_handler(text="Show Product")
async def show_product_handler(message:types.Message):
    products=  database.get_products_by_chat_id(message.chat.id)
    if products:
       for product in products:
           name = product[1]
           photo = product[2]
           count = product[3]
           price = product[4]
           description = product[5]
           await message.answer_photo(photo=photo, 
                                      caption=f"""
Product Name: {name}
Product Count: {count}
Product Price: {price}
Description: {description}""")
    else:
        await message.answer("Product not found")
        

if __name__ == "__main__":
    executor.start_polling(dp,skip_updates=True,on_startup=on_startup,on_shutdown=on_shutdown)


