import textfsm
import pandas as pd

def parse(deviceName, deviceOS, cliCommand, cliResult):
    template_name = "../templates/{}_{}.textfsm".format(deviceOS, "_".join(cliCommand.split(" ")))

    with open(template_name) as template_file:
        template = textfsm.TextFSM(template_file)
    results = template.ParseText(cliResult)

    df = pd.DataFrame(results, columns=[x.lower() for x in template.header])
    
    return df.to_dict('r')
