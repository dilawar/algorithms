-- Diff two action potentials

import System.Environment (getArgs)
import Data.List.Split

data ActionPotential = ActionPotential {
    time :: [Double]
    , volt :: [Double]
    } deriving Show 

nullAP = ActionPotential { time = [], volt = [] }

-- Get action potential from a file. 
{-getAP :: String -> [ ActionPotential ]-}
getAP txt = map tableToActionPotential tables
    where 
        tables = createTables $ map pairUp values
        values = map (\x -> map (\y -> read y :: Double) $ splitOneOf " ,;" x) lines
        lines = filter (/=[]) $ splitOn "\n" txt

-- Given a table like structure, convert it inot ActionPotential
tableToActionPotential table = ActionPotential{ time = fst unzipped
    , volt = snd unzipped
    }
    where
        unzipped = unzip table 

-- GIven a list of values, create a table like structure.
createTables vs = foldl intoTables' emptyTables vs
    where
        emptyTables = map (\y -> [] ) (head vs)
        intoTables' [] [] = []
        intoTables' (c:cs) (a:as) = (c ++ [a]) : intoTables' cs as
        -- Sometime we might get an empty list as element. Ignore it
        -- intoTables' x [] = x

-- Pair up first element of list with rest of the list. For example, 
-- pairUp [1, 2, 3] = [ (1, 2), (1, 3) ]
-- pairUp [1, 2] = [ (1, 2) ]
pairUp :: [a] -> [(a, a)]
pairUp (x:xs) = map (\y -> (x, y)) xs

main = do
    files <- getArgs >>= mapM readFile 
    let aps = map getAP files 
    print aps
    putStrLn "Done"
