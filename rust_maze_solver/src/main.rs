use std::io::{BufRead, BufReader, Result, Write};
use std::fs::File;
use std::collections::HashMap;
use std::collections::VecDeque;

#[derive(Debug, Clone, Copy, Hash, Eq, PartialEq)]
struct Point (usize, usize);

fn parse_input(filename: &str) -> Result<(Vec<Vec<u8>>, Point, Point)> {
    let file = File::open(filename)?;
    let reader = BufReader::new(file);

    let mut all_lines = reader.lines();
    let start_point_line = all_lines.next().unwrap()?;
    let end_point_line = all_lines.next().unwrap()?;

    let start_point = parse_point(&start_point_line);
    let end_point = parse_point(&end_point_line);

    let mut maze = Vec::<Vec<u8>>::new();

    for each_line in all_lines {
        let row = each_line?.split_whitespace()
            .filter(|s| s.chars().all(char::is_numeric))
            .map(|s| s.parse::<u8>().unwrap())
            .collect::<Vec<u8>>();
        // println!("{:?}", row);
        maze.push(row);
    }
    Ok((maze, start_point.unwrap(), end_point.unwrap()))
}

fn parse_point(point_line: &str) -> Result<Point> {
    let coordinate: Vec<_> = 
        point_line.split(|c: char| c == '(' || c == ')' || c == ',')
        .filter(|s| !s.is_empty() && s.chars().all(char::is_numeric))
        .map(|s| s.parse::<usize>().unwrap())
        .collect();
    Ok(Point (coordinate[0], coordinate[1]))
}

fn bfs_directions(maze: Vec<Vec<u8>>, start_point: Point, end_point: Point) -> Option<Vec<String>> {
    let rows = maze.len();
    let cols = maze[0].len();

    let mut visited = vec![vec![false; cols]; rows];
    let mut parent_hash_map = HashMap::<Point, (Point, &str)>::new();
    let mut queue = VecDeque::<Point>::new();

    queue.push_back(start_point);
    visited[start_point.0][start_point.1] = true;

    let directions: Vec<((isize, isize), &str)> = vec![
        ((-1, 0), "Up"),
        ((0,1), "Right"),
        ((0,-1), "Left"),
        ((1, 0), "Down"),
    ];

    while let Some(Point(x,y)) = queue.pop_front() {
        // Check goal state
        if(x,y) == (end_point.0, end_point.1) {
            let mut path: Vec<String> = Vec::new();
            let mut current = end_point;

            while let Some((prev_point, direction)) = parent_hash_map.get(&current) {
                path.push(direction.to_string());
                current = *prev_point;
            }

            path.reverse();
            return Some(path);
        }

        for((dir_x, dir_y), direction) in &directions {
            let new_x = x as isize + dir_x;
            let new_y = y as isize + dir_y;
            // If within the bounds of the maze
            if new_x >= 0 && new_y >= 0 && new_x <= (rows - 1) as isize && new_y <= (cols - 1) as isize {
                // If not visited
                if !visited[new_x as usize][new_y as usize] && (maze[new_x as usize][new_y as usize] == 1 || maze[new_x as usize][new_y as usize] == 0) {
                    visited[new_x as usize][new_y as usize] = true;
                    parent_hash_map.insert(Point (new_x as usize, new_y as usize), (Point (x, y), direction));
                    queue.push_back(Point (new_x as usize, new_y as usize));
                }
            }
        }
    }

    None
}

fn write_to_output(direction: Vec<String>) -> std::io::Result<()>{
    let mut file = File::create("output.txt").expect("Unable to create file!");
    file.write_all(direction.join(", ").as_bytes()).expect("Unable to write to file");
    Ok(())
}

fn main() -> Result<()> {
    let (maze, start_point, end_point) = parse_input("../input.txt").unwrap();
    // println!("{:?} : {:?} : {:?}", maze, start_point, end_point);
    let path_directions = bfs_directions(maze, start_point, end_point);
    // println!("{:?}", path_directions);
    if let Some(path) = path_directions {
        write_to_output(path).expect("Could Not Write To File");
    }
    Ok(())
}