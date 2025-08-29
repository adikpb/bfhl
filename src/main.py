from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import re

app = FastAPI()

FULL_NAME = "adithya_kozham_burath_bijoy"
EMAIL = "adithya.22bce9270@vitapstudent.ac.in"
ROLL_NUMBER = "22BCE9270"
BIRTHDATE = "22112004"
USER_ID = f"{FULL_NAME}_{BIRTHDATE}"


class Payload(BaseModel):
    data: list[str]


def alternating_caps(s: str) -> str:
    return "".join([s[i].upper() if i % 2 else s[i].lower() for i in range(len(s))])


@app.post("/bfhl")
async def bfhl(payload: Payload):
    try:
        arr = payload.data

        even_numbers: list[str] = []
        odd_numbers: list[str] = []
        alphabets: list[str] = []
        special_characters: list[str] = []
        numeric_sum = 0

        all_alpha_chars: list[str] = []

        for item in arr:
            if item.isnumeric():
                try:
                    n = int(item)
                except Exception:
                    special_characters.append(item)
                    continue

                if n % 2 == 0:
                    even_numbers.append(item)
                else:
                    odd_numbers.append(item)
                numeric_sum += n

            elif item.isalpha():
                upper_s = item.upper()
                alphabets.append(upper_s)
                all_alpha_chars.extend(list(item))
            else:
                letters = re.findall(r"[A-Za-z]", item)
                digits = re.findall(r"\d+", item)
                others = re.findall(r"[^A-Za-z0-9]+", item)

                if letters and not digits and not others:
                    upper_s = "".join(letters).upper()
                    alphabets.append(upper_s)
                    all_alpha_chars.extend(letters)
                else:
                    special_characters.append(item)
                    if letters:
                        all_alpha_chars.extend(letters)

        reversed_chars = list(reversed(all_alpha_chars))
        reversed_joined = "".join(reversed_chars)
        concat_string = alternating_caps(reversed_joined)

        response = {
            "is_success": True,
            "user_id": USER_ID,
            "email": EMAIL,
            "roll_number": ROLL_NUMBER,
            "odd_numbers": odd_numbers,
            "even_numbers": even_numbers,
            "alphabets": alphabets,
            "special_characters": special_characters,
            "sum": str(numeric_sum),
            "concat_string": concat_string,
        }

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
