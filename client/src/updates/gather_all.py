import time
from threading import Thread

# local imports
from src.updates import (
    gather_brevetes,
    gather_revtecs,
    gather_sutrans,
    gather_satimps,
    gather_recvehic,
    gather_sunarps,
    gather_soats,
    gather_satmuls,
    gather_sunats,
    gather_jneafil,
    gather_osipteles,
    gather_jnemultas,
)


def gather_threads(dash, all_updates):

    full_response = []

    # log change of dashboard status
    dash.logging(general_status=("Activo", 1))

    threads = []

    # requires manual captcha input (might timeout)
    # threads.append(
    #     Thread(
    #         target=gather_satmuls.gather,
    #         args=(dash, all_updates["satmuls"], full_response),
    #     )
    # )

    # do not require manual captcha input
    threads.append(
        Thread(
            target=gather_brevetes.gather,
            args=(dash, all_updates["brevetes"], full_response),
        )
    )
    # threads.append(
    #     Thread(
    #         target=gather_revtecs.gather,
    #         args=(dash, all_updates["revtecs"], full_response),
    #     )
    # )
    threads.append(
        Thread(
            target=gather_sutrans.gather,
            args=(dash, all_updates["sutrans"], full_response),
        )
    )
    # threads.append(
    #     Thread(
    #         target=gather_satimps.gather,
    #         args=(dash, all_updates["satimps"], full_response),
    #     )
    # )
    # threads.append(
    #     Thread(
    #         target=gather_recvehic.gather,
    #         args=(dash, all_updates["recvehic"], full_response),
    #     )
    # )
    # threads.append(
    #     Thread(
    #         target=gather_sunarps.gather,
    #         args=(dash, all_updates["sunarps"], full_response),
    #     )
    # )
    # threads.append(
    #     Thread(
    #         target=gather_soats.gather,
    #         args=(dash, all_updates["soats"], full_response),
    #     )
    # )
    # threads.append(
    #     Thread(
    #         target=gather_sunats.gather,
    #         args=(dash, all_updates["sunats"], full_response),
    #     )
    # )
    # threads.append(
    #     Thread(
    #         target=gather_jnemultas.gather,
    #         args=(dash, all_updates["jnemultas"], full_response),
    #     )
    # )
    # threads.append(
    #     Thread(
    #         target=gather_jneafil.gather,
    #         args=(dash, all_updates["jneafils"], full_response),
    #     )
    # )
    # threads.append(
    #     Thread(
    #         target=gather_osipteles.gather,
    #         args=(dash, all_updates["osipteles"], full_response),
    #     )
    # )

    # start all threads with a time gap to avoid webdriver conflict
    for thread in threads:
        thread.start()
        time.sleep(1.5)

    # wait for all active threads to finish
    while any([i.is_alive() for i in threads]):
        time.sleep(3)

    # final log update and give time for dashboard to update
    dash.logging(general_status=("Esperando", 2))
    time.sleep(3)

    # return all data that needs to be updated in database in one dictionary
    return full_response
