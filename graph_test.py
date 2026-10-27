import random
import pandas as pd
import plotly.graph_objects as go
import sqlite3, datetime


def get_results():
    db_path = 'database_logins.db'
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    date_now = str(datetime.datetime.now().date()).split('-')[-1] + "." + \
               str(datetime.datetime.now().date()).split('-')[-2]

    arr = cursor.execute(
        f'SELECT results, dates FROM loggins WHERE login ="admin" AND password = "Admin123"').fetchall()
    results = [int(x) for x in arr[0][0].split()]
    results_str = ''
    dates = arr[0][1].split()
    dates_str = ''
    for date in dates:
        dates_str += date + " "
    for result in results:
        results_str += str(result) + " "
    cursor.execute(
        f'UPDATE loggins SET results = "{results_str + " " + str(random.randint(1, 20))}" WHERE login = "admin"')
    cursor.execute(
        f'UPDATE loggins SET dates = "{dates_str + " " + date_now}" WHERE login = "admin"')
    connection.commit()

    arr = cursor.execute(
        f'SELECT results, dates FROM loggins WHERE login ="admin" AND password = "Admin123"').fetchall()
    results = [int(x) for x in arr[0][0].split()]
    dates = arr[0][1].split()

    # ── 1. Данные: ваши результаты по попыткам ──────────────
    data = {
        "attempt": [f"Попытка {i}" for i in range(1, len(dates) + 1)],
        "date": dates,
        "correct": results,  # правильных ответов
    }

    TOTAL = 20
    PASS = 15

    df = pd.DataFrame(data)
    df["label"] = df["attempt"] + "<br>" + df["date"]  # подпись + дата

    # Цвет столбцов: зелёный — порог пройден, оранжевый — нет
    colors = ["#27ae60" if c >= PASS else "#e67e22" for c in df["correct"]]
    best_i = df["correct"].idxmax()  # лучшая попытка

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=df["label"], y=df["correct"],
        marker=dict(color=colors, line=dict(width=1, color="rgba(0,0,0,0.15)")),
        text=[f"{c}/{TOTAL}" for c in df["correct"]],
        textposition="outside",
        textfont=dict(size=14, color="#333333"),
        name="Правильных ответов",
    ))

    fig.add_hline(y=PASS, line_dash="dash", line_color="#c0392b",
                  annotation_text=f"Порог: {PASS}",
                  annotation_font_color="#c0392b")

    fig.add_annotation(
        x=df["label"][best_i], y=df["correct"][best_i] + 0.7,
        text=f"🏆 Лучший результат: {df['correct'][best_i]}/{TOTAL}",
        showarrow=True, arrowhead=2, arrowsize=1.3,
        font=dict(size=15, color="#8e44ad"),
    )

    progress = df["correct"].iloc[-1] - df["correct"].iloc[0]
    fig.add_annotation(
        x=0.01, y=0.98, xref="paper", yref="paper", showarrow=False,
        text=f"Прогресс на последнюю попытку: <b>+{progress}</b> правильных относительно 1-й попытки",
        font=dict(size=14, color="#27ae60"),
        align="left", xanchor="left",
    )

    fig.update_layout(
        template="plotly_white",  # светлая тема
        paper_bgcolor="#ffffff",  # белый фон рисунка
        plot_bgcolor="#f7f9fb",  # светло-серый фон области графика
        title=dict(text="Результаты тестирования: прогресс по попыткам",
                   x=0.5, font=dict(size=24, color="#2c3e50")),
        xaxis_title="Попытка",
        yaxis_title=f"Правильных ответов (из {TOTAL})",
        yaxis=dict(range=[0, TOTAL + 4], gridcolor="#e3e7ec"),
        legend=dict(orientation="h", y=1.1, x=0.5, xanchor="center"),
        font=dict(family="Segoe UI, Arial", size=14, color="#333333"),
        bargap=0.35,
        width=1100, height=650, )

    fig.write_image("test_results_light.png", scale=2)
