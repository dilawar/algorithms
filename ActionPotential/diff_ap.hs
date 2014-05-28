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
getAP txt = createTables $ map pairUp values
    where 
        values = map (\x -> map (\y -> read y :: Float) $ splitOneOf " ,;" x) lines
        lines = splitOn "\n" txt

createTables vs 
    | length vs == 0 = []
    | otherwise = foldl intoTables' emptyTables vs
    where
        emptyTables = map (\y -> [] ) (head vs)

intoTables' [] [] = []
intoTables' (c:cs) (a:as) = (c ++ [a]) : intoTables' cs as
intoTables' x y = error $ "Error. Tables " ++ (show x) ++ " : elems " ++ (show y)


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
