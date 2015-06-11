-- Implementation of Welford method.


import Data.List as L
import System.Random

mean :: Fractional a => [a] -> a
mean xs = (sum xs) / (fromIntegral $ length xs)

variance ls = mean $ map (\x -> (x - u)^2) ls 
    where u = mean ls

online_single_pass :: Fractional a => [a] -> a
online_single_pass (l:ls) = compute ls l l 1 where
        compute (x:xs) sos mean n 
            | null xs = a/(n+1) - u*u
            | otherwise = compute xs a u (n+1) 
            where 
                a = sos + x*x
                u = (n*mean + x)/(n+1)

welford :: Fractional a => [a] -> a
welford (x1:xs) = helper xs 0.0 x1 2 where
    helper (y:ys) var mean n 
        | null ys = newvar 
        | otherwise = helper ys newvar newmean (n+1) where 
            newmean = ((n-1)*mean + y) / n
            newvar = ((n-1)*var + (y - mean)*(y - newmean)) / n

main = do
    seed <- newStdGen
    {-let d = randoms seed :: [Double]-}
    let d = take 20 [1.0,3.5..]
    let var0 = variance d
    let var1 = online_single_pass  d
    let var2 = welford d
    print $ "Variance: " ++ show var0
    print $ "Single pass: " ++ show var1
    print $ "Welford: " ++ show var2
