def parse_to_dataframe(line):
    if('Something messed up' in line):
        return
    else:
        for log_identifier in ['[ERROR]', '[DEBUG]', '[INFO]']:
            if(log_identifier in line):
                log_array = line.split(log_identifier)[0].split(' ')
                log_type = log_identifier.replace('[', '').replace(']', '')
                date = str(log_array[0])
                time = str(log_array[1])
                datetime = date + ' ' + time
                pid = str(log_array[3]).replace('[', '').replace(']', '')
                response_time = str(log_array[4]).replace(
                    '[', '').replace(']', '').replace('ms', '')
                uid = str(log_array[6]).replace(']', '')
                url = line.split(log_identifier)[1].split(' ')[1]
                return [log_type, date,
                        time, datetime, pid, response_time, uid, url]
