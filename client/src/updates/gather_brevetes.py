from datetime import datetime as dt

# local imports
from src.utils.utils import date_to_db_format
from src.scrapers import scrape_brevete


def gather(dash, update_data, full_response):

    CARD = 0

    # log first action
    dash.logging(
        card=CARD,
        title=f"Brevete [{len(update_data)}]",
        status=1,
        progress=0,
        text="Inicializando",
        lastUpdate="Actualizado:",
    )

    # iterate on all records that require updating and get scraper results
    response = []
    for counter, (id_member, doc_tipo, doc_num) in enumerate(update_data):

        # skip member if doc tipo is not DNI (CE mostly) - should have been filtered, double check
        if doc_tipo != "DNI":
            continue

        retry_attempts = 0
        # loop to catch scraper errors and retry limited times
        while retry_attempts < 3:
            try:
                # log action
                dash.logging(card=CARD, text=f"Procesando: {doc_tipo} {doc_num}")

                # send request to scraper
                brevete_response, pimpagas_response = scrape_brevete.browser(
                    doc_num=doc_num
                )

                # update memberLastUpdate table with last update information
                _now = dt.now().strftime("%Y-%m-%d")

                # stop processing if blank response from scraper
                if not brevete_response:
                    dash.logging(
                        card=CARD,
                        status=2,
                        text="Scraper crash",
                        lastUpdate=dt.now(),
                    )
                    return

                # go to next record if no brevete info
                if brevete_response == -1:
                    continue

                # adjust date to match db format (YYYY-MM-DD)
                _n = date_to_db_format(data=brevete_response)

                # add foreign key and current date to scraper response
                response.append(
                    {
                        "Id_Member_FK": id_member,
                        "Clase": _n[0],
                        "Numero": _n[1],
                        "Tipo": _n[2],
                        "FechaExp": _n[3],
                        "Restricciones": _n[4],
                        "FechaHasta": _n[5],
                        "Centro": _n[6],
                        "Puntos": _n[7],
                        "Record": _n[8],
                        "LastUpdate": _now,
                    }
                )

                dash.logging(
                    action=f'[ BREVETES ] {"|".join([str(i) for i in response[-1]])}'
                )

                # process list of papeletas impagas and put them in different table
                for papeleta in pimpagas_response:

                    # adjust date to match db format (YYYY-MM-DD)
                    papeleta_dates_fixed = date_to_db_format(data=papeleta)

                    # add foreign key and current date to response
                    _values = [id_member] + papeleta_dates_fixed + [_now]

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
                    card=CARD, msg=f"< BREVETE > Retrying Record {doc_tipo}-{doc_num}."
                )

        # if code gets here, means scraping has encountred three consecutive errors, skip record
        dash.logging(
            card=CARD, msg=f"|ERROR| No se pudo procesar {doc_tipo} {doc_num}."
        )

    # combine all responses into correct format
    full_response.append({"brevetes": response})

    # log last action
    dash.logging(
        card=CARD,
        title="Brevetes",
        progress=100,
        status=3,
        text="Inactivo",
        lastUpdate=dt.now(),
    )
