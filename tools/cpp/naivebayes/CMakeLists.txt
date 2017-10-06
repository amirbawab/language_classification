project(naivebayes)

# Add  exectuable
add_executable(${PROJECT_NAME} src/naivebayes.cpp)

# Add libraries
target_link_libraries(${PROJECT_NAME} pthread)
