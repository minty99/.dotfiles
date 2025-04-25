local ENGLISH = "com.apple.keylayout.ABC"
local KOREAN = "org.youknowone.inputmethod.Gureum.han2"

function applicationWatcher(appName, eventType, appObject)
    if (eventType == hs.application.watcher.activated) then
        if (appName == "Code") then
            local inputSource = hs.keycodes.currentSourceID()
            if not (inputSource == ENGLISH) then
                hs.keycodes.currentSourceID(ENGLISH)
            end
        end
    end
end

appWatcher = hs.application.watcher.new(applicationWatcher):start()

local esc_bind

function escHandler()
    local inputSource = hs.keycodes.currentSourceID()
        if not (inputSource == ENGLISH) then
                hs.keycodes.currentSourceID(ENGLISH)
        end
        esc_bind:disable()
        hs.eventtap.keyStroke({}, 'escape')
        esc_bind:enable()
end

esc_bind = hs.hotkey.new({}, 'escape', escHandler):enable()
