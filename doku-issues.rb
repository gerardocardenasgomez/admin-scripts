#!/usr/bin/env ruby
# Author: Gerardo Cardenas-Gomez
# Version 0.0.1
# Future plans: 
#

def strip(filename)
    array = filename.split("/")
    splitter = array[-1].index('.txt')
    return array[-1].slice(0, splitter).gsub('_', ' ')
end

def file_search(file, outfile)
    File.open(file) do |f|
        f.each_line do |line|
            if line.include?("FIXME")
                file_append(file, line.chomp, outfile)
            end
        end
    end
end

def file_append(file, line, outfile)
    unless File.read(outfile).include?(line) then
       open(outfile, 'a') { |f| f.puts "[[#{strip(file)}]]-> #{line}\\\\" }
    end
end

root = ARGV[0]
outfile = ARGV[1]

files = Dir.glob("#{root}/*.txt")

for file in files do
    if file =~ /issues.txt/ then
        next
    end

    file_search(file, outfile)
end
