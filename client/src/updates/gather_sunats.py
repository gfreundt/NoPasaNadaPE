from datetime import datetime as dt

# local imports
from src.utils.utils import date_to_db_format
from src.scrapers import scrape_sunat


def gather(dash, update_data, full_update):

    CARD = 8

    # log first action
    dash.logging(
        card=CARD,
        title=f"Sunat [{len(update_data)}]",
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
                sunat_response = scrape_sunat.browser(doc_tipo, doc_num)

                # update memberLastUpdate table with last update information
                _now = dt.now().strftime("%Y-%m-%d")

                # update dashboard with progress and last update timestamp
                dash.logging(
                    card=CARD,
                    progress=int((counter / len(update_data)) * 100),
                    lastUpdate=dt.now(),
                )

                # response ok, no information available
                if sunat_response == -1:
                    dash.logging(
                        action=f"[ SUNATS ] Sin informacion para DNI {doc_num}."
                    )
                    break

                # response ok, information available

                # adjust date to match db format (YYYY-MM-DD)
                _n = date_to_db_format(data=sunat_response)

                # add foreign key and current date to scraper response
                response.append(
                    {
                        "IdMember_FK": id_member,
                        "NumeroRUC": _n[0],
                        "TipoContribuyente": _n[1],
                        "TipoDocumento": _n[2],
                        "NombreComercial": _n[3],
                        "FechaInscripcion": _n[4],
                        "Estado": _n[5],
                        "Condicion": _n[6],
                        "DomicioFiscal": _n[7],
                        "FechaInicioActividades": _n[8],
                        "LastUpdate": _now,
                    }
                )

                dash.logging(
                    action=f"[ SUNATS ] {'|'.join([str(i) for i in response[-1]])}"
                )

                # skip to next record
                break

            except KeyboardInterrupt:
                quit()

            # except Exception:
            #     retry_attempts += 1
            #     dash.logging(
            #         card=CARD,
            #         text=f"|ADVERTENCIA| Reintentando [{retry_attempts}/3]: {doc_num}",
            #     )

    full_update.append({"sunats": response})

    # log last action
    dash.logging(
        card=CARD,
        title="Sunat",
        progress=100,
        status=3,
        text="Inactivo",
        lastUpdate=dt.now(),
    )
