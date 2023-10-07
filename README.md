# qts
Quick interface for roblox-ts.

## Arguments
`-I@owner/package` - Installs the package <br>
`-o` - Output file <br>
`-k` - Do not delete temporary files (for debug) <br>
## Example
`qts test.ts -o test.lua -I@rbxts/services` <br> <br>
compile test.ts with the services package and output to test.lua, it will also generate a `runtime.lua` file and a /include folder with all the dependencies.
## Coming soon
- Support multiple input files
