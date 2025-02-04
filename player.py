from PIL import Image
import pyautogui, pytesseract, keyboard, openai

START = ';'
STOP = ','
KEY = ''
client = openai.OpenAI(api_key = KEY)

answer_coords = {
    'A': (40, 575, 610, 70),  # Answer 1 coordinates
    'B': (660, 575, 600, 70),  # Answer 2 coordinates
    'C': (20, 650, 610, 70),   # Answer 3 coordinates
    'D': (660, 650, 600, 70)   # Answer 4 coordinates
}

def getTxt():
    left, top, width, height = 40, 510, 1200, 60

    left1, top1, width1, height1 = 20, 575, 610, 70
    left2, top2, width2, height2 = 660, 575, 600, 70
    left3, top3, width3, height3 = 20, 650, 610, 70
    left4, top4, width4, height4 = 660, 650, 600, 70


    screenshot = pyautogui.screenshot(region=(left, top, width, height))
    screenshot.save('question.png')
    question = Image.open('question.png')

    screenshot = pyautogui.screenshot(region=(left1, top1, width1, height1))
    screenshot.save('answer1.png')
    answer1 = Image.open('answer1.png')
    screenshot = pyautogui.screenshot(region=(left2, top2, width2, height2))
    screenshot.save('answer2.png')
    answer2 = Image.open('answer2.png')
    screenshot = pyautogui.screenshot(region=(left3, top3, width3, height3))
    screenshot.save('answer3.png')
    answer3 = Image.open('answer3.png')
    screenshot = pyautogui.screenshot(region=(left4, top4, width4, height4))
    screenshot.save('answer4.png')
    answer4 = Image.open('answer4.png')

    q = pytesseract.image_to_string(question).strip()
    ans1 = pytesseract.image_to_string(answer1).strip()
    ans2 = pytesseract.image_to_string(answer2).strip()
    ans3 = pytesseract.image_to_string(answer3).strip()
    ans4 = pytesseract.image_to_string(answer4).strip()

    try:
        print('Question:', q)
        print('Answer 1:', ans1)
        print('Answer 2:', ans2)
        print('Answer 3:', ans3)
        print('Answer 4:', ans4)
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an assistant that helps answer multiple-choice questions."},
                {"role": "user", "content": f"Question: {q}\nOptions:\nA) {ans1}\nB) {ans2}\nC) {ans3}\nD) {ans4}\n\nWhich one is the correct answer? Reply with only A, B, C, or D."}
            ]
        )
        answer = response.choices[0].message.content.strip()
        print("selected answer:", answer)

        x, y, w, h = answer_coords[answer]
        pyautogui.moveTo(x + w // 2, y + h // 2, duration = 0.1)
        pyautogui.click()
        print('clicked ', answer)

    except Exception as e:
        print(e)

    return q, ans1, ans2, ans3, ans4

def main():
    while True:
        if keyboard.is_pressed(START):
            print('ss taken\n')
            getTxt()

        if keyboard.is_pressed(STOP):
            print('stopped')
            break

if __name__ == '__main__':
    main()