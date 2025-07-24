from datetime import datetime as dt

# local imports
from src.scrapers import scrape_sunarp


def gather(dash, update_data):

    CARD = 6

    # log first action
    dash.logging(
        card=CARD,
        title=f"Fichas Sunarp [{len(update_data)}]",
        status=1,
        progress=0,
        text="Inicializando",
        lastUpdate="Actualizado:",
    )

    # iterate on every placa and write to database
    response = []
    for counter, placa in enumerate(update_data, start=1):

        retry_attempts = 0
        # loop to catch scraper errors and retry limited times
        while retry_attempts < 3:
            try:
                # log action
                dash.logging(card=CARD, text=f"Procesando: {placa}")

                # send request to scraper
                image_bytes = scrape_sunarp.browser(placa=placa)

                # update dashboard with progress and last update timestamp
                dash.logging(
                    card=CARD,
                    progress=int((counter / len(update_data)) * 100),
                    lastUpdate=dt.now(),
                )

                # correct captcha, no image for placa - next placa
                if not response:
                    break

                # if there is data in response, enter into database, go to next placa
                _now = dt.now().strftime("%Y-%m-%d")

                # add foreign key and current date to response
                response.append(
                    {
                        "IdPlaca_FK": 999,
                        "PlacaValidate": placa,
                        "Serie": "",
                        "VIN": "",
                        "Motor": "",
                        "Color": "",
                        "Marca": "",
                        "Modelo": "",
                        "Ano": "",
                        "PlacaVigente": "",
                        "PlacaAnterior": "",
                        "Estado": "",
                        "Anotaciones": "",
                        "Sede": "",
                        "Propietarios": "",
                        "ImageBytes": image_bytes,
                        "LastUpdate": _now,
                    }
                )

                # skip to next record
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

    response.update({"sunarps": response})

    # log last action
    dash.logging(
        card=CARD,
        title="Fichas Sunarp",
        status=3,
        progress=100,
        text="Inactivo",
        lastUpdate=dt.now(),
    )


# TODO: move to post-processing
def extract_data_from_image(img_filename):
    return [""] * 13
