# qts
One file compiler for roblox-ts.

## Arguments
`-I@owner/package` - Installs the package
`-o` - Output file
`-k` - Do not delete temporary files (for debug)
## Example
`qts test.ts -o test.lua -I@rbxts/services`
compile test.ts with the services package and output to test.lua, it will also generate a `runtime.lua` file and a /include folder with all the dependencies.
