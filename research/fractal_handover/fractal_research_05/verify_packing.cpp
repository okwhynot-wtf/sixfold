// Independent exact integer verification of every potentially close pair.
// Input: packed little-endian signed int64 triples, then an integer distance D.
// Closed balls of radius (D-1)/2 are strictly separated if this program passes.
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <unordered_map>
#include <vector>

using Point = std::array<int64_t,3>;

int64_t floor_div(int64_t x,int64_t d) {
    int64_t q=x/d,r=x%d;
    return q-(r<0);
}

uint64_t key(int64_t x,int64_t y,int64_t z) {
    constexpr int64_t offset=1LL<<19,limit=1LL<<20;
    x+=offset;y+=offset;z+=offset;
    if(x<0||x>=limit||y<0||y>=limit||z<0||z>=limit)
        throw std::runtime_error("Cell key out of range");
    return uint64_t(x)|(uint64_t(y)<<20)|(uint64_t(z)<<40);
}

int main(int argc,char**argv) {
  try {
    if(argc!=3) throw std::runtime_error("Usage: verify_packing coordinates.i64 D");
    const int64_t d=std::stoll(argv[2]);
    if(d<=0||d>100000000) throw std::runtime_error("Unsafe distance");
    const int64_t d2=d*d;
    std::ifstream input(argv[1],std::ios::binary|std::ios::ate);
    if(!input) throw std::runtime_error("Cannot open coordinate input");
    const auto bytes=input.tellg();
    if(bytes%24!=0) throw std::runtime_error("Truncated coordinate input");
    input.seekg(0);
    const uint64_t count=uint64_t(bytes)/24;
    std::unordered_map<uint64_t,std::vector<Point>> cells;
    cells.reserve(count);
    uint64_t checks=0;
    int64_t minimum=std::numeric_limits<int64_t>::max();
    for(uint64_t index=0;index<count;index++) {
      Point p;
      input.read(reinterpret_cast<char*>(p.data()),24);
      if(!input) throw std::runtime_error("Read failed");
      for(auto v:p) if(v<=-3LL*(1LL<<29)||v>=3LL*(1LL<<29))
          throw std::runtime_error("Coordinate bound failed");
      const int64_t x=floor_div(p[0],d),y=floor_div(p[1],d),z=floor_div(p[2],d);
      for(int dx=-1;dx<=1;dx++) for(int dy=-1;dy<=1;dy++) for(int dz=-1;dz<=1;dz++) {
        const auto it=cells.find(key(x+dx,y+dy,z+dz));
        if(it==cells.end()) continue;
        for(const auto&q:it->second) {
          // Same or adjacent cells give |coordinate difference|<2d.
          // Thus the sum of three squares is <12d^2<1.2e17<2^63.
          int64_t squared=0;
          for(int j=0;j<3;j++) {const int64_t delta=p[j]-q[j];squared+=delta*delta;}
          checks++;
          if(squared<minimum) minimum=squared;
          if(squared<=d2) throw std::runtime_error("Packing separation failed");
        }
      }
      cells[key(x,y,z)].push_back(p);
    }
    std::cout<<"{\"passed\":true,\"points\":"<<count
      <<",\"cell_width\":"<<d<<",\"checked_pairs\":"<<checks
      <<",\"minimum_checked_distance_squared\":"<<minimum
      <<",\"threshold_distance_squared\":"<<d2<<"}\n";
  } catch(const std::exception&e) {std::cerr<<e.what()<<"\n";return 1;}
}
