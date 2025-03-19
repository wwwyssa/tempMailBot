import aiohttp
import asyncio

async def create_temp_email():
    url = "https://api.internal.temp-mail.io/api/v3/email/new"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    data = {
        "min_name_length": 10,
        "max_name_length": 10
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data, headers=headers) as response:
            if response.status == 200:
                email_data = await response.json()
                return email_data['email']
            else:
                print("Ошибка при создании временной почты")
                return None


async def get_emails(email):
    url = f"https://api.internal.temp-mail.io/api/v3/email/{email}/messages"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                messages = await response.json()
                return messages
            else:
                print("Ошибка при получении писем")
                return []


async def main():
    # Создаем временную почту
    temp_email = await create_temp_email()
    if temp_email:
        print(f"Временная почта создана: {temp_email}")

        # Ждем некоторое время для получения писем
        print("Ожидание писем...")
        await asyncio.sleep(60)  # Ждем 60 секунд

        # Получаем письма
        emails = await get_emails(temp_email)
        if emails:
            print("Полученные письма:")
            for email in emails:
                print(f"От: {email['from']}")
                print(f"Тема: {email['subject']}")
                print(f"Текст: {email['body_text']}")
                print("-" * 40)
        else:
            print("Писем нет.")
    else:
        print("Не удалось создать временную почту.")


if __name__ == "__main__":
    asyncio.run(main())