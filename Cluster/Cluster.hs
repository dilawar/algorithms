module Main where

import System.Random 
import qualified Data.List as L
import qualified Data.List.Split as LS

find_clusters vec size = L.group vec

cluster vec k = -- LS.divvy k k newvec
    find_clusters vec k
  where
    newvec = zip vec [0,1..]

main :: IO ( )
main = do
    g <- getStdGen
    let chars =  take 100 $ randomRs ('A', 'E') g
    let res = cluster chars 3
    print $ res
    putStrLn "All done"
