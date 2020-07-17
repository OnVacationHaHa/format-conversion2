import os, csv


def main():
    input_path = os.getcwd() + "\\input_file"
    output_path = os.getcwd() + "\\output_file"
    if os.path.exists(output_path) == False:
        os.makedirs(output_path)
    with open(input_path + '\\node.csv', 'r') as f:
        nodes = f.readlines()
        del nodes[0]
        for i in range(len(nodes)):
            nodes[i] = nodes[i].replace('\n', '')
            nodes[i] = nodes[i].split(',')
    f.close()
    with open(output_path + '\\node.csv', 'w+', newline='') as f:
        writer = csv.writer(f)
        header = ['name', 'node_id', 'zone_id', 'node_type', 'control_type', 'x_coord', 'y_coord']
        writer.writerow(header)
        for node in nodes:
            name = node[0]
            phy_node_id = int(node[1])
            [start_time, end_time] = node[2].split('_')
            start_time = int(start_time)
            end_time = int(end_time)
            x_coord = int(node[4])
            y_coord = int(node[5])
            node_type = node[7]
            control_type = node[8]
            zone_id = int(node[9])
            time_len = time_diff(end_time, start_time)
            now_time = 1
            time_step = int(node[3])
            while (now_time <= time_len):
                newrow = []
                newrow.append(name)
                now_node_id = str(phy_node_id) + "00" + get_HHMM(now_time, start_time)
                newrow.append(now_node_id)
                newrow.append(zone_id)
                newrow.append(node_type)
                newrow.append(control_type)
                newrow.append(x_coord)
                newrow.append(y_coord)
                writer.writerow(newrow)
                now_time += time_step
    f.close()
    with open(input_path + '\\road_link.csv', 'r') as f:
        road_links = f.readlines()
        del road_links[0]
        for i in range(len(road_links)):
            road_links[i] = road_links[i].replace('\n', '')
            road_links[i] = road_links[i].split(',')
    f.close()
    with open(output_path + '\\road_link.csv', 'w+', newline='') as f:
        writer = csv.writer(f)
        header = ['name', 'road_link_id', 'phy_from_node_id', 'phy_to_node_id', 'from_node_id', 'to_node_id', 'facility_type', 'link_type', 'length', 'lanes', 'free_speed',
                  'capacity', 'dir_flag', 'cost', 'geometry']
        writer.writerow(header)
        road_link_id = 1
        for r in road_links:
            name = r[0]
            phy_from_node_id = int(r[2])
            phy_to_node_id = int(r[3])
            [start_time, end_time] = r[4].split('_')
            start_time = int(start_time)
            end_time = int(end_time)
            time_len = time_diff(end_time, start_time)
            time_step = int(r[5])
            travel_time = int(r[6])
            capacity = r[7]
            free_speed = r[8]
            lanes = r[9]
            facility_type = r[10]
            link_type = r[11]
            cost = r[12]
            length = r[13]
            geometry = r[14]
            now_from_time = 1
            while now_from_time <= time_len:
                newrow = []
                newrow.append(name)
                newrow.append(road_link_id)
                road_link_id += 1
                newrow.append(phy_from_node_id)
                newrow.append(phy_to_node_id)
                now_to_time = now_from_time + travel_time
                if now_to_time > time_len:
                    break
                from_node_id=str(phy_from_node_id)+'00'+get_HHMM(now_from_time,start_time)
                to_node_id=str(phy_to_node_id)+'00'+get_HHMM(now_to_time,start_time)
                newrow.append(from_node_id)
                newrow.append(to_node_id)
                newrow.append(facility_type)
                newrow.append(link_type)
                newrow.append(length)
                newrow.append(lanes)
                newrow.append(free_speed)
                newrow.append(capacity)
                newrow.append(1)
                newrow.append(cost)
                newrow.append(geometry)
                now_from_time+=time_step
                writer.writerow(newrow)
    f.close()


def time_diff(now_time, start_time):
    now_time_hour = now_time // 100
    now_time_min = now_time % 100
    start_time_hour = start_time // 100
    start_time_min = start_time % 100
    time_diff = (now_time_hour - start_time_hour) * 60 + now_time_min - start_time_min
    return time_diff


def get_HHMM(now_time, start_time):
    now_time_hour = now_time // 60
    now_time_min = now_time % 60
    start_time_hour = start_time // 100
    start_time_min = start_time % 100
    if now_time_min + start_time_min < 60:
        return_time = (now_time_hour + start_time_hour) * 100 + now_time_min + start_time_min
        if return_time < 1000:
            return '0' + str(return_time)
        else:
            return str(return_time)
    else:
        add_hour = (now_time_min + start_time_min) // 60
        rest_min = (now_time_min + start_time_min) % 60
        return_time = (now_time_hour + start_time_hour + add_hour) * 100 + rest_min
        if return_time < 1000:
            return '0' + str(return_time)
        else:
            return str(return_time)


if __name__ == '__main__':
    main()
