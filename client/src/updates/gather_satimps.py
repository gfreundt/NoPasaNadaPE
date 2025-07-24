from datetime import datetime as dt

# local imports
from src.scrapers import scrape_satimp


def gather(dash, update_data, full_response):

    CARD = 3

    # log first action
    dash.logging(
        card=CARD,
        title=f"Impuestos SAT [{len(update_data)}]",
        status=1,
        progress=0,
        text="Inicializando",
        lastUpdate="Actualizado:",
    )

    # iterate on all records that require updating and get scraper results
    response = []
    for counter, (id_member, doc_tipo, doc_num) in enumerate(update_data, start=1):

        retry_attempts = 0
        # loop to catch scraper errors and retry limited times
        while retry_attempts < 3:
            try:
                # log action
                dash.logging(card=CARD, text=f"Procesando: {doc_tipo} {doc_num}")

                # send request to scraper
                new_records = scrape_satimp.browser(doc_tipo=doc_tipo, doc_num=doc_num)

                # if no error in scrape, delete any prior satimp data of this member in both tables
                _now = dt.now().strftime("%Y-%m-%d")

                for new_record in new_records:

                    response.append(
                        {
                            "IdMember_FK": id_member,
                            "Codigo": new_record["codigo"],
                            "Ano": new_record["deudas"]["ano"],
                            "Periodo": new_record["deudas"]["periodo"],
                            "DocNum": new_record["deudas"]["documento"],
                            "TotalAPagar": new_record["deudas"]["total_a_pagar"],
                            "FechaHasta": new_record["deudas"]["fecha_hasta"],
                            "LastUpdate": _now,
                        }
                    )

                # update dashboard with progress and last update timestamp
                dash.logging(
                    card=CARD,
                    status=1,
                    progress=int((counter / len(update_data)) * 100),
                    lastUpdate=dt.now(),
                )

                # next record
                break

            except KeyboardInterrupt:
                quit()

            # except Exception:
            #     retry_attempts += 1
            #     dash.logging(
            #         card=CARD,
            #         status=2,
            #         text=f"|ADVERTENCIA| Reintentando [{retry_attempts}/3]: {doc_tipo} {doc_num}",
            #     )

        # if code gets here, means scraping has encountred three consecutive errors, skip record
        dash.logging(
            card=CARD, msg=f"|ERROR| No se pudo procesar {doc_tipo} {doc_num}."
        )

    full_response.append({"satimps": response})

    # log last action
    dash.logging(
        card=CARD,
        title="Impuestos SAT",
        progress=100,
        status=3,
        text="Inactivo",
        lastUpdate=dt.now(),
    )
