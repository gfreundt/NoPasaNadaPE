from datetime import datetime as dt

# local imports
from src.scrapers import scrape_jneafil


def gather(dash, update_data, full_response):

    CARD = 9

    # log first action
    dash.logging(
        card=CARD,
        title=f"JNE Afiliacion [{len(update_data)}]",
        status=1,
        progress=0,
        text="Inicializando",
        lastUpdate="Actualizado:",
    )

    # iterate on all records that require updating and get scraper results
    response = []
    for counter, (id_member, doc_tipo, doc_num) in enumerate(update_data, start=1):

        retry_attempts = 0
        while retry_attempts < 3:
            try:
                # log action
                dash.logging(card=CARD, text=f"Procesando: {doc_num}")

                # send request to scraper
                jne_response = scrape_jneafil.browser(doc_num)

                # update memberLastUpdate table with last update information
                _now = dt.now().strftime("%Y-%m-%d")

                # update dashboard with progress and last update timestamp
                dash.logging(
                    card=CARD,
                    progress=int((counter / len(update_data)) * 100),
                    lastUpdate=dt.now(),
                )

                # add foreign key, True/False flag and current date to scraper response
                response.append(
                    {
                        "IdMember_FK": id_member,
                        "Afiliacion": bool(jne_response),
                        "ImageBinary": jne_response,
                        "LastUpdate": _now,
                    }
                )

                dash.logging(
                    action=f"[ JNE Afil ] {'|'.join([str(i) for i in response[-1]])}"
                )

                # next record
                break

            except KeyboardInterrupt:
                quit()

            # except Exception:
            #     retry_attempts += 1
            #     dash.logging(
            #         card=CARD,
            #         text=f"|ADVERTENCIA| Reintentando [{retry_attempts}/3]: {doc_num}",
            #     )

    full_response.append({"jneafil": response})

    # log last action
    dash.logging(
        card=CARD,
        title="JNE Afiliacion",
        progress=100,
        status=3,
        text="Inactivo",
        lastUpdate=dt.now(),
    )
