from selenium import webdriver
import bs4
import pandas as pd

# https://gall.dcinside.com/board/lists/?id=tr&page= #테일즈런너
# https://gall.dcinside.com/board/lists/?id=d_fighter_new1&page= #던파
# https://gall.dcinside.com/board/lists/?id=elsword&page= #엘소드
# https://gall.dcinside.com/board/lists/?id=maplestory&page= #메이플
def seungyun():
    driver = webdriver.Chrome(
        executable_path="../webdriver/chromedriver.exe"
    )
    end = True
    id = []
    numbers = []
    nickname = []
    count = []
    reply = []
    for i in range(1, 10000):
        url = "https://gall.dcinside.com/board/lists/?id=maplestory&page=" + str(i)

        driver.get(url)  # 주소 입력후 enter
        pageString = driver.page_source
        soup = bs4.BeautifulSoup(pageString, "html.parser")
        pageTitle = soup.findAll("tr", {"class": "ub-content us-post"})

        for trs in pageTitle:
            td = trs.find("td", {"class": "gall_writer ub-writer"})
            tds = trs.find("td", {"class": "gall_tit ub-word"})
            galldate = trs.find("td", {"class": "gall_date"}).text
            gallcount = int(trs.find("td", {"class": "gall_count"}).text)
            gallid = td.get('data-uid')
            notice = trs.find("td", {"class": "gall_num"}).text

            if notice == '공지':
                continue
            num = int(notice)

            if galldate == "08.31": #날짜 지정
                end = False
                break

            if num in numbers:
                pass
            else:
                try:
                    recount = tds.find("span")
                    if recount:
                        intrecount = int(recount.text[1:-1])
                        reply.append(intrecount)
                    else:
                        recount = 0
                        reply.append(recount)

                    span = td.find("span").text
                    numbers.append(num)
                    count.append(gallcount)
                    nickname.append(span)
                    id.append(gallid)

                except:
                    pass

        if (end == False):
            break

    df = pd.DataFrame(nickname, columns=['nickname'])
    df['id'] = id
    df['count'] = count
    df['reply'] = reply
    df.to_csv("C:/test/test1.csv", encoding='utf-8-sig')

def seungyun2():
    df = pd.read_csv("C:/test/test1.csv", encoding='utf-8-sig', index_col=0)
    df = df.fillna('DC')

    avg = df["count"].groupby([df["id"], df["nickname"]])  # 평균 조회수
    replyg = df["reply"].groupby([df["id"], df["nickname"]])  # 평균 리플수

    avg2 = df.groupby(['id', 'nickname'])['nickname'].count()
    avg3 = pd.DataFrame(avg2)
    avg3.to_csv("C:/test/test2.csv", encoding='utf-8-sig')

    newdf = pd.read_csv("C:/test/test2.csv", encoding='utf-8-sig')
    newdf.rename(columns={'id': '아이디', 'nickname': '닉네임', 'nickname.1': '글수'}, inplace=True)
    aaa = newdf.sort_values(by='글수', ascending=False)
    abc = pd.DataFrame(round(avg.mean()))
    replyavg = pd.DataFrame(round(replyg.mean(),2))

    abc.rename(columns={'id': '아이디', 'nickname': '닉네임', 'count': '평균조회수'}, inplace=True)
    replyavg.rename(columns={'id': '아이디', 'nickname': '닉네임', 'reply': '평균댓글수'}, inplace=True)
    gall = pd.merge(aaa, abc, left_on=['아이디', '닉네임'], right_index=True)
    final = pd.merge(gall, replyavg, left_on=['아이디', '닉네임'], right_index=True)
    final = final[final['글수'] > 20]
    final.to_csv("C:/test/final.csv", encoding='utf-8-sig')


seungyun()
seungyun2()
