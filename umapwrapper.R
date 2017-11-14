

Rumap <- function(data, verbose = FALSE, tmpinput = NULL, tmpoutput = NULL, statsoutput = NULL,
                  n.neighbors=15, n.components =2, metric='euclidean',
                  gamma = 1.0, alpha = 1.0, min.dist = 0.1, spread = 1.0, debug = FALSE) {

    if (is.null(tmpinput))
        tmpinput <- tempfile();

    if (is.null(tmpoutput))
        tmpoutput <- tempfile();

    if (is.null(statsoutput))
        statsoutput <- tempfile();

    if (debug) {
        cat(paste0('tmpinput=',tmpinput),'\n');
        cat(paste0('tmpoutput=',tmpoutput), '\n');
        cat(paste0('statsoutput=',statsoutput),'\n');
    }
    
    if (verbose) cat('Writing data... ');
    write.table(data, file=tmpinput, quote = F, row.names = F, col.names =T)
    if (verbose) cat('done\n');

    if (verbose) cat('Running external umap script...');
    cmd.params <- paste0(
        ' --inputcsv ', tmpinput,
        ' --output ', tmpoutput,
        ' --statsfile ', statsoutput,
        ' --n_neighbors ', n.neighbors,
        ' --n_components ', n.components,
        ' --metric ', metric,
        ' --gamma ', gamma,
        ' --alpha ', alpha,
        ' --min_dist ', min.dist,
        ' --spread ', spread,
        ' '
    )

    exec.path <- './umapwrapper.py'
    
    cmd <- paste0(exec.path, cmd.params)

    if (debug) {
        cat('\n');
        cat(paste0('Executing command: \n', cmd, '\n'))
    }
    
    retval <- system(cmd)
    if (retval != 0) {
        stop(paste0('An error occured! Return value: ', retval));
    }
    
    if (verbose) cat('done\n')

    if (verbose) cat('Reading embedding...');
    emb <- read.csv(tmpoutput, header=F)
    rownames(emb) <- rownames(data)
    if (verbose) cat('done\n');

    if (verbose) cat('Reading stats...');
    runtime <- scan(statsoutput);
    if (verbose) cat('done\n')

    # Return value
    list(embedding=emb,runtime=runtime[1])
}
