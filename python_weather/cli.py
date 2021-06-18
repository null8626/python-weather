from halo import Halo
halo_ = Halo(spinner='lines', text='please wait...', color='white').start()
client_ = None

from python_weather import Client, HTTPException
from typing import Optional
from asyncio import get_event_loop
from sys import argv, exit

flags = [
    ('help', 'Shows this help screen.'),
    ('unit C | F | METRIC | IMPERIAL', 'Sets the measuring unit to metric (default) or imperial.'),
    ('locale <LANG>', 'Sets the default locale. Defaults to en-US.'),
    ('output <PATH>', 'Outputs the data to a JSON file instead.'),
    ('center', 'Positions the text to be the center of the terminal window.')
]

argv = tuple(map(str.lower, argv[1:]))

class CLI(Client):
    __slots__ = tuple()

    def __init__(self):
        pass
    
    @property
    def client(self) -> Optional[Client]:
        global client_
        return client_

    @property
    def halo(self) -> "Halo":
        global halo_
        return halo_
    
    @property
    def location(self) -> Optional[str]:
        value = ''
        for arg in argv:
            if arg[0] == '-': return value[1:]
            value += ' ' + arg
        return value[1:]

    async def throw_err(self, message: str) -> None:
        self.halo.stop()
        print(f"\033[91merror: {message}\033[0m")
        if self.client:
            await self.client.close()
        exit(1)

    def get_arg(self, value: str) -> tuple:
        full = f'-{value[0]}' if f'-{value[0]}' in argv else f'--{value}'
        if full not in argv:
            return False, ''

        val = ''
        for part in argv[argv.index(full) + 1:]:
            if part[0] == '-':
                return True, val[1:]
            val += ' ' + part
        return True, val[1:]

    def display_help(self) -> None:
        global flags

        flags_str = ''
        for flag, description in flags:
            flag_name = flag.split(' ')[0]
            flags_str += f'\n  -\033[1m{flag_name[0]}\033[0m | --\033[1m{flag_name}\033[0m -> \033[1m{description}\033[0m\n  usage: \033[1m-{flag_name[0]} {flag[len(flag_name) + 1:]}\033[0m\n'

        self.halo.stop()
        print(f"\033[0;0Husage: \033[1m'weather <location> [...flags]'\033[0m\nflags:{flags_str[:-1]}")

    async def run(self) -> None:
        need_help, _ = self.get_arg('help')
        if need_help:
            return self.display_help()
        
        if not self.location:
            await self.throw_err("please add a location. run 'weather -h' for details.")

        _, unit = self.get_arg('unit')
        if unit and unit not in ('c', 'f', 'metric', 'imperial'):
            await self.throw_err("invalid unit. a unit must be 'c', 'f', 'metric', or 'imperial'.")
        
        unit = ('c' if (unit or 'metric') == 'metric' else 'f' if unit != 'c' else 'c').upper()
        _, locale = self.get_arg('locale')

        global client_
        client_ = Client(format=unit, locale=locale or "en-US")
        
        try:
            self.halo.text = f"requesting weather forecast for '{self.location}'..."
            response = await self.client.find(self.location)
        except HTTPException as http_err:
            await self.throw_err(f"error: {http_err.message.lower()}")

        self.halo.text = "formatting..."

        from datetime import datetime
        from re import findall
        
        current = response.current
        obj = {
            "location": response.location_name,
            "coordinates": f"{response.latitude}, {response.longitude}",
            "provider": response.provider,
            "temperature": f"{current.temperature} °{unit}",
            "feels like": f"{current.feels_like} °{unit}",
            "sky text": current.sky_text,
            "humidity": f"{current.humidity}%",
            "wind speeds": f"{current._get('@windspeed') or 'unknown'}",
            "date": datetime.strftime(current.date, f"%A, %d %B %Y at %H:%M:%S (UTC{'+' if response.timezone_offset > -1 else ''}{response.timezone_offset})"),
            "url": response.url
        }

        forecast_objects = {}
        forecast_objects_last_key = None
        for forecast in response.forecasts:
            formatted_date = datetime.strftime(forecast.date, f"%A, %d %B %Y at %H:%M:%S (UTC{'+' if response.timezone_offset > -1 else ''}{response.timezone_offset})")
            forecast_objects_last_key = formatted_date
            forecast_objects[formatted_date] = {
                "lowest temperature": f"{forecast.low} °{unit}",
                "highest temperature": f"{forecast.high} °{unit}",
                "sky text": forecast.sky_text,
                "precipitation": f"{forecast.precip}%" if forecast.precip else "unknown"
            }

        _, json_path = self.get_arg('output')
        if json_path:
            from json import dumps
            from os.path import isfile
            from re import search

            obj['forecasts'] = forecast_objects
            if not search(r'.json[/\\]?$', json_path):
                json_path += ".json"
            
            try:
                f = open(json_path, 'w+')
                f.write(dumps(obj).replace('\\u00b0', '°')) # why
                f.close()
            except Exception as err:
                await self.throw_err(err)
            self.halo.stop()
            print(f"\x1B[1m\x1B[32msuccess: saved json output in '{json_path}'.\x1B[39m\x1B[22m")
            return await self.client.close()

        centered_text, _ = self.get_arg('center')
        if centered_text:
            from os import get_terminal_size

        max_key_length = get_terminal_size().columns // 2 if centered_text else (max([
            *map(len, obj.keys()),
            *map(len, forecast_objects[forecast_objects_last_key].keys())
        ]) + 5)

        string = '\n'
        for key, value in obj.items():
            string += f"\x1B[90m{' ' * (max_key_length - len(key))}{key}\x1B[39m: \033[1m{value}\033[0m\n"

        for match in findall(r'https?://\S+', string):
            string = string.replace(match, f'\x1B[36m{match}\x1B[0m')
        
        if response.alert_message:
            string = f"\x1B[33m{' ' * (max_key_length - 5)}alert: {response.alert_message}\x1B[39m\n" + string

        for key, value in forecast_objects.items():
            if centered_text:
                string += f"\n{' ' * (max_key_length - ((len(key) + 2) // 2))}[{key}]\n"
            else:
                string += f"\n{' ' * max_key_length}  [{key}]\n"
            
            for k, v in value.items():
                string += f"\x1B[90m{' ' * (max_key_length - len(k))}{k}\x1B[39m: \033[1m{v}\033[0m\n"

        self.halo.stop()
        print(string[:-1])
        await self.client.close()

def main():
    cli = CLI()
    get_event_loop().run_until_complete(cli.run())

if __name__ == "__main__":
    main()