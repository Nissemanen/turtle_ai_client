local config = require("config")

print("Connecting...")
local ws, err = http.websocket(config.host)

if not ws then
    print("Failed to connect: ".. tostring(err))
    return
end

ws.send(textutils.serialiseJSON({
    type = "hello",
    capabilities = {"geo_scan"}
}))

local msg = ws.receive()
local server_hello = textutils.unserialiseJSON(msg)

if server_hello.type ~= "hello" then
    print("Unexpected first message from server")
    return
end

print("Connected")

local function handle_message(msg)
    return
end

while true do
    ws.send(textutils.serialiseJSON({
        type="state"
    }))

    local response = ws.receive()

    if response then
        local cmd = textutils.unserialiseJSON(response)
        print("Got: "..cmd.action)
    end

    os.sleep(3)
end