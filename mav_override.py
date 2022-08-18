from pymavlink import mavutil

# Start a connection listening on a UDP port

the_connection = mavutil.mavlink_connection('tcp:localhost:5763')

# Wait for the first heartbeat 
# This sets the system and component ID of remote system for the link

the_connection.wait_heartbeat()
print("Heartbeat from system (system %u component %u)" % (the_connection.target_system, the_connection.target_component))


the_connection.mav.request_data_stream_send(the_connection.target_system, the_connection.target_component,
                                        mavutil.mavlink.MAV_DATA_STREAM_ALL, 1, 1)

#

def set_rc_channel_pwm_roll_pitch(pwm_roll=1500,pwm_pitch=1500):
    """ Set RC channel pwm value
    Args:
        channel_id (TYPE): Channel ID
        pwm (int, optional): Channel pwm value 1100-1900
    """


    # Mavlink 2 supports up to 18 channels:
    # https://mavlink.io/en/messages/common.html#RC_CHANNELS_OVERRIDE
    rc_channel_values = [65535 for _ in range(18)]
    rc_channel_values[0]=pwm_roll;#Setting pwm values for channel 1 (roll)
    rc_channel_values[1]=pwm_pitch;#Setting pwm values for channel 2 (pitch)
    the_connection.mav.rc_channels_override_send(
    the_connection.target_system,                # target_system
    the_connection.target_component,             # target_component
        *rc_channel_values)                  # RC channel list, in microseconds.

while 1:
    set_rc_channel_pwm_roll_pitch(1600,1400)
    msg = the_connection.recv_match(type='RC_CHANNELS',blocking=True)
    print(msg)
    