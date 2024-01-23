-- Hijack Ardupilot PWM and convert to MASCP Packets

-- Initialize Serial
local port = serial:find_serial(0)

if not port or baud == 0 then
    gcs:send_text(0, "No Scripting Serial Port")
    return
end

port:begin(115200)
port:set_flow_control(0)

local function get_thruster_PWMs()
  pwm1 = SRV_Channels:get_output_pwm(33) -- motor 1
  pwm2 = SRV_Channels:get_output_pwm(34) -- motor 2
  pwm3 = SRV_Channels:get_output_pwm(35) -- motor 3
  pwm4 = SRV_Channels:get_output_pwm(36) -- motor 4
  pwm5 = SRV_Channels:get_output_pwm(37) -- motor 5
  pwm6 = SRV_Channels:get_output_pwm(38) -- motor 6
  -- gcs:send_text(7, "T1:" .. tostring(pwm1) .. " T2:" .. tostring(pwm2).. " T3:" .. tostring(pwm3).. " T4:" .. tostring(pwm4).. " T5:" .. tostring(pwm5).. " T6:" .. tostring(pwm6))
  return { pwm1, pwm2, pwm3, pwm4, pwm5, pwm6 }
end

-- Notify topside that motors are working.
gcs:send_text(6, "Initialized MASCP")
function update()
  for i, pulse_width in pairs(get_thruster_PWMs()) do
    -- Send address byte of MASCP packet (49-54)
    port:write(48 + i)
    -- Send throttle byte of MASCP packet (0-255)
    -- Convert from PW (1100-1900) to byte.
    port:write(math.floor(255*(pulse_width-1100)/800))
  end
  return update, 10
end

return update()