import csv
import requests
from bs4 import BeautifulSoup

# How do we find it:
# - Programme
# ul.ev-act-schedule__performances
# li.ev-act-schedule__performance-composer-segments
#### Composer name: a.ev-act-schedule__work-composer-name
#### Piece name: span.ev-act-schedule__performance-work-name
#### Duration: span.ev-act-schedule__performance-work-duration
#### Notes: span.ev-act-schedule__performance-work-note
###### Just get all text? All elements? List of text?

"""
Each day:
li.ev-event-calendar__single-date-events 

    - Each date:
    h3.ev-event-calendar__date

    Each concert:
    li.ev-event-calendar__event-summary-container

        - Each time: 
        div.ev-event-calendar__time

        - Concert name:
        div.ev-event-calendar__name > a.text

        - Venue:
        span.ev-event-calendar__event-location

        Hidden details:
        div.ev-event-calendar__description-and-schedule

        Within that the details are:
        li.ev-event-calendar__information

        Container for each piece
        li.ev-act-schedule__performance-composer-segments

            - Composer:
            a.ev-act-schedule__work-composer-name

            - Piece name:
            span.ev-act-schedule__performance-work-name

            - Duration:
            span.ev-act-schedule__performance-work-duration

            - Notes:
            span.ev-act-schedule__performance-work-note

"""

with open("proms_composer_data_all.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f, delimiter="|")
    for year in range(1895, 2022):
        url = f"https://www.bbc.co.uk/proms/events/by/date/{year}"
        html = requests.get(url).content
        soup = BeautifulSoup(html, "lxml")

        # Each day
        day_query_tree = soup.find_all(
            "li", class_="ev-event-calendar__single-date-events"
        )

        for date in day_query_tree:
            # Date:
            try:
                date_query = date.find(
                    "h3", class_="ev-event-calendar__date"
                ).text.strip()
            except:
                date_query = "//"
            # Each concert that day
            concert_query_tree = date.find_all(
                "div", class_="ev-event-calendar__information"
            )

            for concert in concert_query_tree:
                # Time:
                try:
                    time_query = concert.find(
                        "div", class_="ev-event-calendar__time"
                    ).text.strip()
                except:
                    time_query = "//"

                # Concert Name:
                try:
                    concert_name_query = concert.find(
                        "div", class_="ev-event-calendar__name"
                    ).text.strip()
                except:
                    concert_name_query = "//"

                # Venue Name:
                try:
                    venue_query = concert.find(
                        "span", class_="ev-event-calendar__event-location"
                    ).text.strip()
                except:
                    venue_query = "//"

                # Piece query tree
                try:
                    piece_query_tree = concert.find_all(
                        "li", class_="ev-act-schedule__performance-composer-segments"
                    )
                except:
                    piece_query_tree = "//"

                for piece in piece_query_tree:
                    # Check if Interval, if so continue
                    try:
                        if piece.find(
                            "span",
                            class_="ev-act-schedule__performance-segment-interval",
                        ):
                            continue
                    except:
                        pass

                    # Composer:
                    try:
                        composer_query = piece.find(
                            "a", class_="ev-act-schedule__work-composer-name"
                        ).text.strip()
                    except:
                        composer_query = "//"

                    # Piece name:
                    try:
                        piece_query = piece.find(
                            "span", class_="ev-act-schedule__performance-work-name"
                        ).text.strip()
                    except:
                        piece_query = "//"

                    # Duration:
                    try:
                        duration_query = piece.find(
                            "span", class_="ev-act-schedule__performance-work-duration"
                        ).text.strip()[1:-1]
                    except:
                        duration_query = "//"

                    # Notes:
                    try:
                        note_query = piece.find(
                            "span", class_="ev-act-schedule__performance-work-note"
                        ).text.strip()
                    except:
                        note_query = "//"

                    writer.writerow(
                        [
                            date_query,
                            time_query,
                            concert_name_query,
                            venue_query,
                            composer_query,
                            piece_query,
                            duration_query,
                            note_query,
                        ]
                    )
