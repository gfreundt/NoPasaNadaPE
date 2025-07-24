from datetime import datetime as dt

# local imports
from src.utils.utils import date_to_db_format
from src.scrapers import scrape_sutran


def gather(dash, update_data, full_response):

    CARD = 7

    # log first action
    dash.logging(
        card=CARD,
        title=f"Sutran [{len(update_data)}]",
        status=1,
        progress=0,
        text="Inicializando",
        lastUpdate="Actualizado:",
    )

    # iterate on all records that require updating and get scraper results
    response = []
    for counter, placa in enumerate(update_data, start=1):

        retry_attempts = 0
        # loop to catch scraper errors and retry limited times
        while retry_attempts < 3:
            try:
                # log action
                dash.logging(card=CARD, text=f"Procesando: {placa}")

                # send request to scraper
                sutran_response = scrape_sutran.browser(placa=placa)

                _now = dt.now().strftime("%Y-%m-%d")

                # update dashboard with progress and last update timestamp
                dash.logging(
                    card=CARD,
                    progress=int((counter / len(update_data)) * 100),
                    lastUpdate=dt.now(),
                )

                # if response is blank, skip to next placa
                if not sutran_response:
                    break

                # iterate on all multas
                for resp in sutran_response:
                    _n = date_to_db_format(data=resp)

                    response.append({"PlacaValidate": placa, "Documento":_n[0], "Tipo":_n[1], "FechaDoc":_n[2], "CodigoInfrac":_n[3], "Clasificacion":_n[4], "LastUpdate":_now})

                    # insert gathered record of member
                    dash.logging(
                        action=f"[ SUTRANS ] {"|".join([str(i) for i in response[-1]])}"
                    )

                # no errors - next placa
                break

            except KeyboardInterrupt:
                quit()

            # except Exception:
            #     retry_attempts += 1
            #     dash.logging(
            #         card=CARD,
            #         text=f"|ADVERTENCIA| Reintentando [{retry_attempts}/3]: {placa}",
            #     )

        # if code gets here, means scraping has encountred three consecutive errors, skip record
        dash.logging(card=CARD, msg=f"|ERROR| No se pudo procesar {placa}.")

    # combine all responses into correct format
    full_response.append({"sutrans": response})

    # log last action
    dash.logging(
        card=CARD,
        title="Sutran",
        progress=100,
        status=3,
        text="Inactivo",
        lastUpdate=dt.now(),
    )
