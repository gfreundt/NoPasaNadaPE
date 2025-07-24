from datetime import datetime as dt

# local imports
from src.scrapers import scrape_recvehic


def gather(dash, update_data, full_update):

    CARD = 1

    # log first action
    dash.logging(
        card=CARD,
        title=f"Record Conductor [{len(update_data)}]",
        status=1,
        progress=0,
        text="Inicializando",
        lastUpdate="Actualizado:",
    )

    # iterate on all records that require updating and get scraper results
    response=[]
    for counter, (id_member, doc_tipo, doc_num) in enumerate(update_data, start=1):

        # records are only available for members with DNI
        if doc_tipo != "DNI":
            continue

        retry_attempts = 0
        # loop to catch scraper errors and retry limited times
        while retry_attempts < 3:
            try:
                # log action
                dash.logging(card=CARD, text=f"Procesando: {doc_tipo} {doc_num}")

                # send request to scraper
                pdf_bytes = scrape_recvehic.browser(doc_num=doc_num)

                # update memberLastUpdate table with last update information
                _now = dt.now().strftime("%Y-%m-%d")

                # response from scraper is that there is no record
                if pdf_bytes == -1:
                    break

                # stop process if blank response from scraper
                if not pdf_bytes:
                    dash.logging(
                        card=CARD,
                        status=2,
                        text="Scraper crash",
                        lastUpdate=dt.now(),
                    )
                    return

                # add foreign key and current date to response
                response.append({"IdMember_FK":id_member, "PDFBytes":pdf_bytes, "LastUpdate":_now})

                # delete all old records from member
                dash.logging(action=f"[ RECORD ] {"|".join([str(i) for i in response[-1]])}")

                # update dashboard with progress and last update timestamp
                dash.logging(
                    card=CARD,
                    progress=int((counter / len(update_data)) * 100),
                    lastUpdate=dt.now(),
                )

                # no errors - next member
                break

            except KeyboardInterrupt:
                quit()

            except Exception:
                retry_attempts += 1
                dash.logging(
                    card=CARD,
                    status=2,
                    text=f"|ADVERTENCIA| Reintentando [{retry_attempts}/3]: {doc_tipo} {doc_num}",
                )

    full_update.append({"recvehic":response})

    # log last action
    dash.logging(
        card=CARD,
        title="Record del Conductor",
        progress=100,
        status=3,
        text="Inactivo",
        lastUpdate=dt.now(),
    )
