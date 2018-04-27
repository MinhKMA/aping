from pprint import pprint
import asyncio
import re
import time
from pprint import pprint
from aioinflux import InfluxDBClient


data = {'linh': {'HTTP': ['192.168.100.30', '192.168.40.120'],
          'PING': ['192.168.40.120']},
 'locvu': {'HTTP': ['2.2.3.2',
                    '1.2.3.2',
                    '2.2.23.2',
                    '192.168.40.116',
                    '231.12.12.3',
                    '4.6.8.9'],
           'PING': ['2.2.3.2', '2.2.3.2', '1.2.3.2']},
}

fping_re = re.compile(
        r"(?P<host>[^ ]+)\s*:.+=\s*(?P<sent>\d+)/(?P<recv>\d+)/(?P<loss>\d+)"
        r"(.+=\s*(?P<min>[0-9.]+)/(?P<avg>[0-9.]+)/(?P<max>[0-9.]+))?")


def get_process(data):
    cmd = []
    base_cmd = [
        "fping",
        "-c", "20"
    ]
    for user in data:
        cmd.append(' '.join(base_cmd + data[user]['PING']))
    return cmd

async def run_command(*args):
    # Create subprocess
    process = await asyncio.create_subprocess_shell(
        *args,
        # stdout must a pipe to be accessible as process.stdout
        stderr=asyncio.subprocess.PIPE)
    # Wait for the subprocess to finish
    stdout, stderr = await process.communicate()
    # Return stdout
    return stderr.decode().strip()



def read_lines():
    cmds = get_process(data=data)
    loop = asyncio.get_event_loop()
    commands = []
    for cmd in cmds:
        commands.append(run_command(cmd))
    results = loop.run_until_complete(asyncio.gather(*commands))
    pprint(results)
    # for result in results:
    #     data_match = fping_re.match(result.decode("utf-8").strip())



start = time.time()
read_lines()
end = time.time()
print('Total: {}'.format(end - start))



