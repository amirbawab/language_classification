project(csv2csv)

# Add ngram exectuable
add_executable(${PROJECT_NAME} src/csv2csv.cpp)

# Add libraries
target_link_libraries(${PROJECT_NAME} pthread)
