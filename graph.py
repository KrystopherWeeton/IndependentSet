    #? Results have been collected. Create dir and plot results
    for n_value in n:
        dir_name: str = generate_results_directory(n_value, num_trials)
        dir_name = create_dir(dir_name, agressive=True)

        # Code block to show 3d map of results
        l_values, k_values, z = results.get_results(n_value)
        plot.graph_heatmap(
            x=l_values,
            y=k_values,
            z=z,
            directory=dir_name,
            file_name="heatmap",
            min="0",
            max=str(results.planted_sizes[n_value]),
            title=f"Size of Intersection with Planted Independent Set (n={n_value}, size={planted_ind_set_size(n_value)}) \n after Local Optimization on Headstart Set",
            x_axis_title="Size of Headstart Set (l)",
            y_axis_title="Size of Intersection in Headstart Set (k)"
        )